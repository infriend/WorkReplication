"""
Test pattern match, word field and machine learning method.
All need text data, for world field and ml, we need text and its corresponding entity.
"""
import pickle

import dataprocess.readdata
import dataprocess.vocabulary
import dataprocess.ltpprocess
import extractmethod.patternmatch
import extractmethod.wordfield
import extractmethod.machinelearning
import dataprocess.datalabeling
import numpy as np

# Read test texts
texts, testentitydict = dataprocess.readdata.read_texts("test")  # get texts and entities
# ns_sentences, ns_poses = dataprocess.readdata.get_allns("test")  # get ns sentences' segs and poses
# word_f = dataprocess.vocabulary.word_frequency(texts)
ns_sentences = np.load("./data/testdata/test_ns_sentences.npy", allow_pickle=True).item()
ns_poses = np.load("./data/testdata/test_ns_poses.npy", allow_pickle=True).item()
word_f = np.load("./data/testdata/testwordfrequency.npy", allow_pickle=True).item()
wordfield = np.load("./data/wordfield.npy", allow_pickle=True).item()
X_Sentences, X_Poses, Y_label = dataprocess.datalabeling.datalabeling(ns_sentences, ns_poses, "test")

triples = []
# Pattern Match and Word Field
for index in texts:
    sentences = dataprocess.ltpprocess.cut_sent(texts[index])
    seg_list, pos_list = dataprocess.ltpprocess.ltp_process(sentences)
    triple = extractmethod.patternmatch.position_patternmatch(X_Sentences[int(index)], X_Poses[int(index)])
    triples += list(set(triple))
    triple = extractmethod.wordfield.extract_field(wordfield, seg_list, pos_list, testentitydict[index])
    triples += list(set(triple))

# Machine Learning
# X, Y = extractmethod.machinelearning.get_feature(X_Sentences, X_Poses, Y_label, word_f, wordfield)
X = np.load("./data/testdata/test_x.npy")
Y = np.load("./data/testdata/test_y.npy")
triple = extractmethod.machinelearning.model_test(X, X_Sentences, testentitydict)
triples += list(set(triple))

entity = []
relation = ''
for t in triples:
    relation += t[0] + ' ' + 'at' + ' ' + t[2] + '\n'
    entity.append(t[0])
    entity.append(t[2])

with open("./data/relation.txt", 'a+') as f:
    f.write(relation)
    f.close()

entity = set(entity)
with open("./data/entity.txt", 'a+') as f:
    for e in entity:
        f.write(e + '\n')
    f.close

print("Finish")
