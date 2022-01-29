import numpy as np
import dataprocess.datalabeling
import extractmethod.machinelearning
import extractmethod.wordfield
import dataprocess.readdata
import dataprocess.vocabulary

# word field
ns_sentences, ns_poses = dataprocess.readdata.get_allns("train")
texts, testentitydict = dataprocess.readdata.read_texts("train")
word_frequency = dataprocess.vocabulary.word_frequency()
wordfield = extractmethod.wordfield.construct_wordfield()
np.save("./data/wordfield.npy", wordfield)

# machine learning
X_Sentences, X_Poses, Y_label = dataprocess.datalabeling.datalabeling(ns_sentences, ns_poses, "train")
word_frequency = np.load("./data/trainingdata/word_frequency_training.npy", allow_pickle=True).item()
wordfield = np.load("./data/wordfield.npy", allow_pickle=True).item()
X, Y = extractmethod.machinelearning.get_feature(X_Sentences, X_Poses, Y_label, word_frequency, wordfield)
eclf = extractmethod.machinelearning.model_train(X, Y)
print("A")