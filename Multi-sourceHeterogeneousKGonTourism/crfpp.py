import os

def train():
    command = "crf_learn -c 10.0 ./data/trainingdata/template ./data/trainingdata/train.data model"
    os.system(command)


def test():
    command = "crf_test"
    os.system(command)
