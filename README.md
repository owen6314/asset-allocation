# asset-allocation
Course Project of EECS E6895: an RL-based asset allocation and recommendation system (US).

## Project Summary
The purpose of this project is to design and implement an asset recommendation system to let users buy traditional assets and cryptocurrency at the same time. The system takes in a combined datasets of stock, ETF and cryptocurrencies, as well as the user's preference on value return or risk. Then the system will give these inputs to two state-of-the-art, model-free reinforcement learning models, one is the policy gradient model proposed by Jiang et al. and the other is the deep Q-learning model. Each model will generate a report with suggested purchasing plan (in the form of weight vectors and their corresponding assets) and indicators, the system will choose the strategy that better fits the user’s preference and output it to the user.

The system is a web application based on AWS (Amazon Web Services).

## File Structure

### ./data
Stores the data processing related code. The data/fetch contains python scripts we use to get information for different types of assets, you can simply run each python scripts in the sub-folder. The data/process contains how we transform the txt format historical price into csv and database. 

### ./system
This stores the actual code for building our recommendation system. The specific file structure is as follows:

system/DQN stores the deep Q learning model's code, system/DQN/data contains the csv input for the algorithms. More details is in README.md in system/DQN. The entire model can be run with the wrap.sh script.

system/PGPortfolio stores the code of EIIE model, the entire model can be run with the pipeline.py. See system/PGPortfolio/README for details.

system/frontend contains the html, css and javascript needed to build the frontend. 

system/lf.py is the python code for the lambda function on AWS. You need to manually create an API Gateway to connect the lambda function to frontend.


See [course webpage](http://www.ee.columbia.edu/~cylin/course/bigdata/projects/) for more details (technical report, slides...). Our project code is 202005-13.
