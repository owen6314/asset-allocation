import pickle
import time
import numpy as np
import argparse
import re

from envs import TradingEnv
from agent import DQNAgent
from utils import get_data, get_scaler, maybe_make_dir, plot_all

# stock_name = "all"
stock_name = "70-small"



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--episode', type=int, default=2000,
                        help='number of episode to run')
    parser.add_argument('-b', '--batch_size', type=int, default=32,
                        help='batch size for experience replay')
    parser.add_argument('-i', '--initial_invest', type=int, default=20000,
                        help='initial investment amount')
    parser.add_argument('-m', '--mode', type=str, required=True,
                        help='either "train" or "test"')
    parser.add_argument('-w', '--weights', type=str, help='a trained model weights')
    args = parser.parse_args()    

    d = vars(args)
    init_asset = d['initial_invest']
    print("Initial asset amount =", init_asset)

    maybe_make_dir('weights')
    maybe_make_dir('portfolio_val')

    timestamp = time.strftime('%Y%m%d%H%M')

    data = get_data(stock_name)
    #print(data.shape[1])
    train = round(data.shape[1]*0.9)
    # test = round(data.shape[1]*0.99)
    # train = 979
    test = 979
    print("train:{}, test:{}".format(data[:, train-1], data[:, test]))
    train_data = data[:, :test]
    test_data = data[:, test:]
    print("test data size: ", len(test_data))

    env = TradingEnv(train_data, args.initial_invest)
    state_size = env.observation_space.shape
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    scaler = get_scaler(env)

    portfolio_value = []

    if args.mode == 'test':
        # remake the env with test data
        env = TradingEnv(test_data, args.initial_invest)
        # load trained weights
        agent.load(args.weights)
        # when test, the timestamp is same as time when weights was trained
        timestamp = re.findall(r'\d{12}', args.weights)[0]
        # daily_portfolio_value = [env.init_invest]
        daily_portfolio_value = []

    for e in range(args.episode):
        state = env.reset()
        state = scaler.transform([state])
        for time in range(env.n_step):
            action = agent.act(state)
            next_state, reward, done, info = env.step(action)
            next_state = scaler.transform([next_state])
            if args.mode == 'train':
                agent.remember(state, action, reward, next_state, done)
            if args.mode == "test":
                daily_portfolio_value.append(info['cur_val'])
            state = next_state
            if done:

                if args.mode == "test" and e % 100 == 0:
                    plot_all(stock_name, daily_portfolio_value, env, test + 1)

                daily_portfolio_value = []
                # print("new_stock_owned is: ", info['new_stock_owned'])
                # print("cash_in_hand is: ", env.cash_in_hand)
                # print("new_stock_price is: ", info['new_stock_price'])    
                final_stock_hold = env.stock_owned
                print("episode: {}/{}, episode end value: {}".format(
                    e + 1, args.episode, info['cur_val']))
                portfolio_value.append(info['cur_val']) # append episode end portfolio value

                break
            if args.mode == 'train' and len(agent.memory) > args.batch_size:
                agent.replay(args.batch_size)
        if args.mode == 'train' and (e + 1) % 10 == 0:  # checkpoint weights
            agent.save('weights/{}-{}-dqn.h5'.format(init_asset,timestamp))
            agent.save('weights/{}-{}.txt'.format(init_asset,timestamp))
            print('./weights/{}-{}-dqn.h5'.format(init_asset,timestamp))

    
    diffArray = np.diff(np.array([x - init_asset for x in portfolio_value]))
    diffArray = np.insert(diffArray, 0, portfolio_value[0]-init_asset, axis=0)

    # print("=======diffArray = ", diffArray)
    diffRatio = diffArray/portfolio_value
    # print("diffRatio = ", diffRatio)

    print("sharpe:", np.mean(diffRatio)/np.std(diffRatio))
    print("fapv:", portfolio_value[-1]/init_asset)

    """calculate the max drawdown with the portfolio changes
    @:param pc_array: all the portfolio changes during a trading process
    @:return: max drawdown
    """
    pc_array = diffArray

    portfolio_values = []
    drawdown_list = []
    max_benefit = 0
    for i in range(len(portfolio_value)-1):
        # if i == 0: continue
        # print(i)
        if i > 0:
            portfolio_values.append(portfolio_value[i])
            # print("the new portfolio_values is: ",portfolio_values)

        else:
            portfolio_values.append(pc_array[i])
        if portfolio_values[i] > max_benefit:
            # print("current value is: ", portfolio_values[i])
            max_benefit = portfolio_values[i]
            # print("the max_benefit is: ",max_benefit)

            drawdown_list.append(0.0)
        else:
            if max_benefit != 0:
                drawdown_list.append(1.0 - portfolio_values[i] / max_benefit)

    drawdown_list[0] = 0
    # print(drawdown_list)
    print("mdd:", max(drawdown_list))


    print("num_of_stock_share: ", final_stock_hold)
    total_stock = sum(final_stock_hold)
   
    # leaves only 5
    weight_vector = [(final_stock_hold[i]/total_stock) for i in range(len(final_stock_hold))]
    print("weight_vector:", weight_vector)



    # save portfolio value history to disk
    with open('portfolio_val/{}-{}.p'.format(timestamp, args.mode), 'wb') as fp:
        pickle.dump(portfolio_value, fp)
