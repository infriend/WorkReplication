import os




def train():
    command = "crf_learn "
    os.system(command)


def test():
    command = "crf_test"
    os.system(command)
