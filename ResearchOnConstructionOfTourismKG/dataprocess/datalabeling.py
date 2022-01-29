"""
Labeling every ns in the triple as 1, others as 0
"""
import numpy as np
import dataprocess.readdata
import dataprocess.ltpprocess
import re
import copy

def datalabeling(all_ns_sentences, all_pos, status):
    """
    Compare the triple entity with all ns sentence, sentences have entity as 1, else as 0
    :return: X: Sentences, Y: Labels
    """
    if status == "train":
        triples_dict, triple_sentences = dataprocess.readdata.read_triple("train")
    else:
        triples_dict, triple_sentences = dataprocess.readdata.read_triple("test")

    combinedSentence = {}
    combinedPoses = {}

    X_Sentences = {}
    X_Poses = {}
    Y_label = {}

    for index in triples_dict:
        entities = []
        X_Sentences.update({index: []})
        X_Poses.update({index: []})
        combinedSentence.update({index: []})
        combinedPoses.update({index: []})
        Y_label.update({index: []})
        sentences_segs = all_ns_sentences[str(index)]
        sentences_pos = all_pos[str(index)]

        for t in triples_dict[index]:
            entities.append(t[0])
            entities.append(t[2])

        entities = set(entities)

        # combine the ns word, save the long ns word.
        for sid in range(len(sentences_segs)):
            # A new sentence
            combinedSentence[index].append([])
            combinedPoses[index].append([])

            ns_word = ''
            positivetime = 0
            negtivetime = 0
            ns_wordlist = []
            for wid in range(len(sentences_segs[sid])):
                if sentences_pos[sid][wid] != 'ns':
                    combinedSentence[index][-1].append(sentences_segs[sid][wid])
                    combinedPoses[index][-1].append(sentences_pos[sid][wid])
                    continue

                # if ns, combine the word and pos
                while wid < len(sentences_segs[sid]) and sentences_pos[sid][wid] == 'ns':
                    ns_word += sentences_segs[sid][wid]
                    wid += 1
                wid -= 1

                combinedSentence[index][-1].append(ns_word)
                combinedPoses[index][-1].append('ns')

                ns_wordlist.append(ns_word)
                ns_word = ''

        # For each sentence, search the ns word, search the entity in the long ns word, if find, set positive.
        for sid in range(len(combinedSentence[index])):
            for wid in range(len(combinedSentence[index][sid])):
                if combinedPoses[index][sid][wid] == 'ns':
                    e_flag = 0
                    X_Sentences[index].append(copy.deepcopy(combinedSentence[index][sid]))
                    X_Sentences[index][-1][wid] = '↑' + combinedSentence[index][sid][wid] + '↑'
                    X_Poses[index].append(combinedPoses[index][sid])
                    for e in entities:
                        match = re.search(e, combinedSentence[index][sid][wid])
                        if match:
                            positivetime += 1
                            Y_label[index].append(1)
                            e_flag = 1
                            break
                    if e_flag == 0:
                        negtivetime += 1
                        Y_label[index].append(0)

    return X_Sentences, X_Poses, Y_label