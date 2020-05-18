# System
system/DQN stores the deep Q learning model's code, system/DQN/data contains the csv input for the algorithms. More details is in README.md in system/DQN. The entire model can be run with the wrap.sh script.

system/PGPortfolio stores the code of EIIE model, the entire model can be run with the pipeline.py. See system/PGPortfolio/README for details.

system/frontend contains the html, css and javascript needed to build the frontend. 

system/lf.py is the python code for the lambda function on AWS. You need to manually create an API Gateway to connect the lambda function to frontend.
