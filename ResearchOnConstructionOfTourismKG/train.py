import numpy as np
import dataprocess.datalabeling
import extractmethod.machinelearning

# word field

# machine learning
X_Sentences, X_Poses, Y_label = dataprocess.datalabeling.datalabeling()
word_frequency = np.load("./data/trainingdata/word_frequency_training.npy", allow_pickle=True).item()
wordfield = np.load("./data/wordfield.npy", allow_pickle=True).item()
X, Y = extractmethod.machinelearning.get_feature(X_Sentences, X_Poses, Y_label, word_frequency, wordfield)
eclf = extractmethod.machinelearning.model_train(X, Y)
print("A")