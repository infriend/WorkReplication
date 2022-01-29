import re
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import VotingClassifier
import pickle
import dataprocess.ltpprocess
import dataprocess.datalabeling

"""
We need data that has label whether its ns can be the attribute value or not, we predict the sentence as 0 or 1.
"""

trainPath = "./data/trainingdata/"
pos_weight = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'g': 6, 'h': 7, 'i': 8,
              'j': 9, 'k': 10, 'm': 11, 'n': 12, 'nd': 13, 'nh': 14, 'ni': 15, 'nl': 16,
              'ns': 17, 'nt': 18, 'nz': 19, 'o': 20, 'p': 21, 'q': 22, 'r': 23, 'u': 24,
              'v': 25, 'wp': 26, 'ws': 27, 'x': 28, 'z': 29}
negativewords = []
with open("./data/negatives/myallnegs.txt", 'r') as f:
    text = f.read()
    negativewords = text.split('\n')
    f.close()

triggerwords = []
with open("./data/triggers_filtered.txt", 'r') as f:
    text = f.read()
    triggerwords = text.split('\n')
    f.close()

def get_feature(X_Sentences, X_Poses, Y_label, word_frequency, wordfield):
    """
    Get the sentence and the ns word, for 1 sentence, get all the entity's feature, else ns as 0;
    for 0 sentence, get all ns feature.
    :param X_Sentences: a dict with form {id: [str0, str1...]}
    :return: X_Feature, np.array
    """
    X_Feature = np.array([np.zeros(28)])
    Y = []
    # for text
    for index in X_Sentences:
        print("Get text %d features" % index)
        sentences = X_Sentences[index]

        # for each feature sentence
        for sid in range(len(sentences)):
            current_sentence = sentences[sid]
            current_pos = X_Poses[index][sid]
            feature = np.zeros(28)
            # scan the word
            for wid in range(len(current_sentence)):
                # Start calculate the feature
                if current_sentence[wid][0] == '↑':
                    currentword = current_sentence[wid].replace('↑', '')
                    # word frequency and pos
                    tempwid = 5
                    while tempwid > 0:
                        if wid - tempwid >= 0:
                            feature[5 - tempwid] = word_frequency[current_sentence[wid - tempwid]]
                            feature[15 - tempwid] = pos_weight[current_pos[wid - tempwid]]
                        tempwid -= 1

                    tempwid = 0
                    while tempwid < 5:
                        if wid + tempwid + 1 < len(current_sentence):
                            feature[5 + tempwid] = word_frequency[current_sentence[wid + tempwid + 1]]
                            feature[15 + tempwid] = pos_weight[current_pos[wid + tempwid + 1]]
                        tempwid += 1
                    feature[20] = len(current_sentence[wid]) - 2
                    feature[21] = wordfield[currentword] if currentword in wordfield else 0
                    feature[22] = 1 if current_pos[wid-1] == 'wp' else 0

                    tempwid = 3
                    while tempwid > 0:
                        if wid - tempwid >= 0:
                            if current_sentence[wid - tempwid] in negativewords:
                                feature[23] = 1
                                break
                        tempwid -= 1

                    w_flag = 0  # if had scanned the vi
                    for tempwid in range(len(current_sentence)):
                        if current_sentence[tempwid] == currentword:
                            if w_flag == 0:
                                feature[24] = tempwid
                                w_flag = 1
                            else:
                                feature[25] = tempwid

                        if feature[26] == 0:
                            feature[26] = 1 if current_sentence[tempwid] in triggerwords else 0
                            feature[27] = abs(wid-tempwid) if feature[26] == 1 else 0
                    X_Feature = np.row_stack((X_Feature, feature))
                    Y.append(Y_label[index][sid])
                    break
    X_Feature = np.delete(X_Feature, [0], axis=0)
    Y = np.array(Y)

    return X_Feature, Y


def model_train(X, Y):
    """
    DT, NB, RF, AB, voting for result, now we train the model.
    :return: fitted clf, for saving the model
    """
    clf0 = DecisionTreeClassifier(criterion="entropy")
    clf1 = GaussianNB()
    clf2 = RandomForestClassifier(n_estimators=80)
    dt_stump = DecisionTreeClassifier(max_depth=1, min_samples_leaf=1)
    clf3 = AdaBoostClassifier(base_estimator=dt_stump)

    eclf = VotingClassifier(
        estimators=[('dt', clf0), ('nb', clf1), ('rf', clf2), ('ab', clf3)], voting='hard'
    )

    scaler = StandardScaler().fit(X)
    X_scale = scaler.transform(X)

    with open("./data/scaler.pkl", 'wb') as f:
        pickle.dump(scaler, f)
        f.close()


    eclf.fit(X_scale, Y)

    with open("./data/eclf.pkl", 'wb+') as f:
        pickle.dump(eclf, f)
        f.close()

    return eclf


def model_test():
    return
