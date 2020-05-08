from __future__ import absolute_import
import json
import time
import datetime
import sys
import logging
import os
import pandas as pd
from pgportfolio.tools.configprocess import load_config


def preprocess_config(config):
    fill_default(config)
    return config


def fill_default(config):
    set_missing(config, "random_seed", 0)
    set_missing(config, "agent_type", "NNAgent")
    fill_layers_default(config["layers"])
    fill_input_default(config["input"])
    fill_train_config(config["training"])


def fill_train_config(train_config):
    set_missing(train_config, "fast_train", True)
    set_missing(train_config, "decay_rate", 1.0)
    set_missing(train_config, "decay_steps", 50000)


def fill_input_default(input_config):
    set_missing(input_config, "save_memory_mode", False)
    set_missing(input_config, "portion_reversed", False)
    set_missing(input_config, "norm_method", "absolute")
    set_missing(input_config, "is_permed", False)
    set_missing(input_config, "fake_ratio", 1)


def fill_layers_default(layers):
    for layer in layers:
        if layer["type"] == "ConvLayer":
            set_missing(layer, "padding", "valid")
            set_missing(layer, "strides", [1, 1])
            set_missing(layer, "activation_function", "relu")
            set_missing(layer, "regularizer", None)
            set_missing(layer, "weight_decay", 0.0)
        elif layer["type"] == "EIIE_Dense":
            set_missing(layer, "activation_function", "relu")
            set_missing(layer, "regularizer", None)
            set_missing(layer, "weight_decay", 0.0)
        elif layer["type"] == "DenseLayer":
            set_missing(layer, "activation_function", "relu")
            set_missing(layer, "regularizer", None)
            set_missing(layer, "weight_decay", 0.0)
        elif layer["type"] == "EIIE_LSTM" or layer["type"] == "EIIE_RNN":
            set_missing(layer, "dropouts", None)
        elif layer["type"] == "EIIE_Output" or\
                layer["type"] == "Output_WithW" or\
                layer["type"] == "EIIE_Output_WithW":
            set_missing(layer, "regularizer", None)
            set_missing(layer, "weight_decay", 0.0)
        elif layer["type"] == "DropOut":
            pass
        else:
            raise ValueError("layer name {} not supported".format(layer["type"]))


def set_missing(config, name, value):
    if name not in config:
        config[name] = value


def parse_time(time_string):
    return time.mktime(datetime.strptime(time_string, "%Y/%m/%d").timetuple())


if __name__ == "__main__":
    initial_asset = int(sys.argv[1])
    import pgportfolio.autotrain.generate as generate
    logging.basicConfig(level=logging.INFO)
    generate.add_packages(load_config(), 1)
    import pgportfolio.autotrain.training
    pgportfolio.autotrain.training.train_all(1, "cpu", initial_asset)
    result = {}
    # mdd, fapv, sharpe, weight_vector
    import pgportfolio.resultprocess.plot
    metrics = pgportfolio.resultprocess.plot.get_metrics(load_config(), ['1'], ['1'], format=None)
    result = metrics
    result_file = "./train_package/train_summary.csv"
    df = pd.read_csv(result_file)
    weight_vector_str = df.iloc[0]['weight_vector']
    weight_vector = weight_vector_str.split(',')
    weight_vector.pop()
    result['weight_vector'] = weight_vector
    with open('model1-500000.json', 'w') as f:
        json.dump(result, f)


