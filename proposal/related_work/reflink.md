# Reference

## background
- what is asset allocation: https://www.thebalance.com/asset-allocation-basics-357311
- past works (mostly before 2000): https://www.sciencedirect.com/science/article/pii/S1059056003000510

## strategy
- AI for portfolio management overview: https://medium.com/swlh/ai-for-portfolio-management-from-markowitz-to-reinforcement-learning-cffedcbba566

- github code + data + paper summary: https://github.com/firmai/machine-learning-asset-management

## recommendation
- asset allocation recommendation: https://www.calcxml.com/calculators/inv01
- another asset allocation calculator: https://www.bankrate.com/calculators/retirement/asset-allocation.aspx

### simple/single factor
- MaxReturnsAgent
- MinVarianceAgent
- MaxSharpeAgent
- MaxDecorrelationAgent

### Reinforcement learning
- 1. [deep RL + EIIE topology] A Deep Reinforcement Learning Framework for the Financial Portfolio Management Problem
papaer link: https://arxiv.org/pdf/1706.10059.pdf,
github: https://github.com/ZhengyaoJiang/PGPortfolio, https://github.com/sonaam1234/PGPortfolio. 
Note: it uses back-test

- [MaxReturn, Maxsharpe agents, etc.]: https://medium.com/swlh/ai-for-portfolio-management-from-markowitz-to-reinforcement-learning-cffedcbba566
github: https://github.com/Rachnog/Deep-Portfolio-Management/blob/master/agent.py

- [easy PG implementation]: https://github.com/liangzp/Reinforcement-learning-in-portfolio-management- 

- source 8: Model-based Deep Reinforcement Learning for Dynamic Portfolio Optimization, https://arxiv.org/pdf/1901.08740.pdf
- DQN: Jin O, El-Saawy H. Portfolio management using reinforcement learning[J]. Stanford University, 2016.

- source 9: deep q learning， G. Jeong and H. Y. Kim. Improving financial trading decisions using deep Q-learning: Predicting the number of shares, action strategies, and transfer learning. Expert system with applications, 117:125–138, 2019.

Du et al. [47] use Q-Learning (without a neural network) in discretized market states to optimize a portfolio of a riskless asset (cash) and a risky asset (stock market portfolio) with transaction costs considered at each rebalancing period. 

- Summary link:
https://github.com/Draichi/Portfolio-Management-list
file:///Users/lintianyi/Desktop/data-04-00110-v2.pdf


## Dataset
- ETFs from Stanford course: https://stanford.edu/class/ee103/portfolio.html
- S&P500 stock kaggle: https://www.kaggle.com/camnugent/sandp500 & https://github.com/selimamrouni/Deep-Portfolio-Management-Reinforcement-Learning/blob/master/data_pipe.ipynb
- cryptocurrencies data - poloniex: https://github.com/selimamrouni/Deep-Portfolio-Management-Reinforcement-Learning/tree/master/poloniex_data & 
  https://github.com/selimamrouni/Deep-Portfolio-Management-Reinforcement-Learning/blob/master/data_pipe_poloniex.ipynb
- crypto-compare.com: need to email to get access--> https://data.cryptocompare.com/data/historical
- Top 100 Cryptocurrencies by Market Capitalization: https://coinmarketcap.com/


## Paper writing reference
- [Use as intro ]The Effect of Cryptocurrency on Investment Portfolio Effectiveness: http://www.sciencepublishinggroup.com/journal/paperinfo?journalid=171&doi=10.11648/j.jfa.20170506.14

- [Use as intro/why we want to do crypto-curr]: Cryptocurrency: A new investment opportunity?https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=6783&context=lkcsb_research

- [past literature review]: Deep Reinforcement Learning-based Portfolio Management By NITIN KANWAR: https://rc.library.uta.edu/uta-ir/bitstream/handle/10106/28108/KANWAR-THESIS-2019.pdf?sequence=1&isAllowed=y
