# EIIE Model

This is the implementation of the EIIE model in our project, which is based on the codebase of paper [A Deep Reinforcement Learning Framework for the Financial Portfolio Management Problem](https://github.com/ZhengyaoJiang/PGPortfolio).

## How to Run
We support Python 3.5+ on Mac. (other platforms not tested)

### Install Dependencies
`pip install -r requirements.txt`

### Run Pipeline
To run the whole pipeline including training and backtest and generate results for the system, use:

 `python pipeline.py <asset_amount>`

Before running the pipeline, please make sure you have the correct-format Data.db under `database/`. Data used in our project could be fetched and processed using the scripts provided.
  
### User Guide
For more functions the model provides, please check out the modified [User Guide](user_guide.md).

## Acknowledgement
Most of the code are inspired by Zhengyao Jiang et al's repo [PGPortfolio](https://github.com/ZhengyaoJiang/PGPortfolio). We modified some modules of the code and network in order to fit in our dataset (e.g. different trading frequency, different sets of assets etc.).

Other algorithms for comparision purpose are based on Li and Hoi's toolkit [OLPS](https://github.com/OLPS/OLPS).
