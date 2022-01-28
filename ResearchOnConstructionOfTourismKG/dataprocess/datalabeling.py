"""
Labeling every ns in the triple as 1, others as 0
"""
import numpy as np
import dataprocess.readdata
import dataprocess.ltpprocess
import re

def datalabeling():
    """
    Compare the triple entity with all ns sentence, sentences have entity as 1, else as 0
    :return: X: Sentences, Y: Labels
    """
    all_ns_sentences = np.load("./all_ns_sentences.npy", allow_pickle=True).item()
    all_pos = np.load("./all_ns_poses.npy", allow_pickle=True).item()
    triples_dict, triple_sentences = dataprocess.readdata.read_triple("train")
    totalnum = 0
    posnum = 0
    X_Sentences = {}
    Y_label = {}

    for index in triples_dict:
        print("Text %d" % index)
        entities = []
        X_Sentences.update({index: []})
        Y_label.update({index: []})
        sentences_segs = all_ns_sentences[str(index)]
        sentences_pos = all_pos[str(index)]

        for t in triples_dict[index]:
            entities.append(t[0])
            entities.append(t[2])

        entities = set(entities)

        # combine the ns word, search the entity in the long ns word, if find, set positive, save the long ns word.
        for sid in range(len(sentences_segs)):
            temp_sentence = ''
            ns_word = ''
            positivetime = 0
            negtivetime = 0
            ns_wordlist = []
            for wid in range(len(sentences_segs[sid])):

                if sentences_pos[sid][wid] != 'ns':
                    temp_sentence += sentences_segs[sid][wid]
                    continue

                while wid < len(sentences_segs[sid]) and sentences_pos[sid][wid] == 'ns':
                    ns_word += sentences_segs[sid][wid]
                    wid += 1
                wid -= 1
                temp_sentence += ns_word
                ns_wordlist.append(ns_word)

                e_flag = 0
                for e in entities:
                    match = re.search(e, ns_word)
                    if match:
                        positivetime += 1
                        Y_label[index].append(1)
                        e_flag = 1
                        break
                if e_flag == 0:
                    negtivetime += 1
                    Y_label[index].append(0)

            for i in range(positivetime+negtivetime):
                X_Sentences[index].append([temp_sentence, ns_wordlist[i]])

    return X_Sentences, Y_label