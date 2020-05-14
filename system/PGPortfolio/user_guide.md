# User Guide
## Configuration File
Under the `nntrader/nntrader` directory, there is a json file called `net_config.json`,
 holding all the configuration of the agent and could be modified outside the program code.
### Network Topology
* `"layers"`
    * layers list of the CNN, including the output layer
    * `"type"`
        * domain is {"ConvLayer", "FullyLayer", "DropOut", "MaxPooling",
        "AveragePooling", "LocalResponseNormalization", "SingleMachineOutput",
        "LSTMSingleMachine", "RNNSingleMachine"}
    * `"filter shape"`
        * shape of the filter (kernal) of the Convolution Layer
* `"input"`
    * `"window_size"`
        * number of columns of the input matrix
    * `"coin_number"`
        * number of rows of the input matrix
        * noted that we already extended the assets types to all kinds of assets, so it doesn't have to be cryptocurrencies
    * `"feature_number"`
        * number of features (just like RGB in computer vision)
        * domain is {1, 2, 3}
        * 1 means the feature is ["close"], last price of each period
        * 2 means the feature is ["close", "volume"]
        * 3 means the features are ["close", "high", "low"]


## Training and Tuning the hyper-parameters
1. First, modify the `nntrader/nntrader/net_config.json` file.
2. make sure current directory is under `nntrader` and type `python main.py --mode=generate --repeat=1`
    * this will make 1 subfolders under the `train_package`
    * in each subfolder, there is a copy of the `net_config.json`
    * `--repeat=n`, n could followed by any positive integers. The random seed of each the subfolder is from 0 to n-1 sequentially.
      * Notably, random seed could also affect the performance in a large scale.
3. type `python main.py --mode=train --processes=1 --asset=<amount>`
    * this will start training one by one of the n folder created just now
    * "--processes=n" means start n processes running parallely.
    * Each training process is made up from 2 stages:
      
4. after that, check the result summary of the training in `nntrader/train_package/train_summary.csv`
5. tune the hyper-parameters based on the summary, and go to 1 again.

## Save and Restore of the Model
* The trained weights of the network are saved at `train_package/1` named as `netfile` (including 3 files). 
