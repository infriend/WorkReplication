import os


def train():
    command = "crfpplearn "
    os.system(command)


def test():
    command = "crfpptest"
    os.system(command)
