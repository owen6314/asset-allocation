# Introduction

This repo is for the DQN part.

# How to run

## Dependencies

Python 3.6

`pip install -r requirements.txt`

## Run

**To train a Deep Q agent**, run `python run.py --mode train`. There are other parameters and I encourage you look at the `run.py` script. After training, a trained model as well as the portfolio value history at episode end would be saved to disk.

**To test the model performance**, run `python run.py --mode test --weights <trained_model>`, where `<trained_model>` points to the local model weights file. Test data portfolio value history at episode end would be saved to disk.

abbreviation|para|default|usage
---|---|---|---
-e | --episode| default=2000 |number of episode to run
-b |--batch_size| default=32 |batch size for experience replay
-i |--initial_invest |default=20000 | initial investment amount
-m |--mode'| required=True |either "train" or "test"
-w |--weights| required when mode = "test" | a trained model weights

Example:
* train: `python run.py --mode train`
* test: `python test.py --mode test --weights ./weights/201912141307-dqn.h5 -e 500`

Run in the bundle:

* use wrap.sh, and the results will be stored in results.json

## Structure
```python
|-data
|-portfolio_val
|-visualization
|-weights
|-requirements.txt
|-agent.py
|-envs.py
|-model.py
|-run.py
|-utils.py
```
* `/data`: the csv files of stock table and history close price of 19 stocks. The files are generated on preprocessing part.
* `/weights`: the files stored weights trained by DQN
* `/visualization`: figures of visualization
* `/portfolio_val`: the portfolio values during episodes when trading or testing
* `agent.py`: a Deep Q learning agent
* `envs.py`: a simple 3-stock trading environment
* `model.py`: a multi-layer perceptron as the function approximator
* `utils.py`: some utility functions
* `run.py`: train/test logic
* `requirement.txt`: all dependencies



# Ref

The structure of code is mainly inspired by [ShuaiW](https://github.com/ShuaiW/teach-machine-to-trade).
