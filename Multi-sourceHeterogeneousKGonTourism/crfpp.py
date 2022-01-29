import os

def crftrain():
    command = "crf_learn -c 4.0 ./data/trainingdata/template ./data/trainingdata/train.txt ./data/model"
    os.system(command)


def crftest():
    command = "crf_test -m ./data/model ./data/testdata/test.txt"
    r = os.popen(command)
    info = r.readlines()

    return info

