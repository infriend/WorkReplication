"""
Search all the at relation's corresponding sentence，get its v, v+p, then identify its effectiveness by hand.
Search all the synonyms of the words above.

For negative words, first handmade a small vocabulary, then use synonyms to expand it.

We only use =.
"""
import re
import dataprocess.ltpprocess
import dataprocess.readdata
import numpy as np

negativewords_sample = []
with open("../data/negatives/negatives01.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        negativewords_sample.append(line.split('\n')[0])  # \n or \t
    f.close()

synonyms = []
synonymPath = '../data/synonyms.txt'
with open(synonymPath, 'r') as f:
    lines = f.readlines()
    for line in lines:
        synonyms.append(line)
    f.close()


# input all the at relation sentence, use ltp to seg, pos with v or v+p
def at_vocabulary(seg_list, pos_list):
    """
    Input all the at relation sentences, out put word list.
    :param sentences: at relation sentences
    :return: at relation's trigger word list
    """
    triggerwords = []
    wordres = []

    # for each sentence
    for i in range(len(seg_list)):
        # for each word
        for j in range(len(seg_list[i])):
            if pos_list[i][j] == 'v':
                if j < len(seg_list[i])-1:
                    if pos_list[i][j+1] == 'p':
                        triggerwords.append(seg_list[i][j]+seg_list[i][j+1])
                    else:
                        triggerwords.append(seg_list[i][j])
                else:
                    triggerwords.append(seg_list[i][j])
            else:
                pass

    for trigger in triggerwords:
        syns = search_syn(trigger)
        wordres += list(syns)

    res = set(wordres)

    return list(res)


def neg_vocabulary():
    res = []
    i = 0
    for neg in negativewords_sample:
        syns = search_syn(neg)
        res += list(syns)
        print(i)
        i += 1

    return set(res)


def search_syn(word):
    """
    Search the word syn in the synonyms.txt, if find, append the syns, else do nothing.
    We use all the words at level 4.
    :return: words and their syns.
    """
    wordlist = []
    for i in range(len(synonyms)):
        match_gen = re.finditer(" " + word + " ", synonyms[i])
        try:
            match = next(match_gen)
        except StopIteration:
            pass
        else:
            # get words before current line
            temp = i - 1
            while synonyms[temp][:5] == synonyms[i][:5]:
                syns = synonyms[i].replace('\n', '').split(" ")
                if syns[0][-1] == '=':
                    wordlist += syns[1:]
                temp -= 1

            # get words after current line
            temp = i + 1
            while synonyms[temp][:5] == synonyms[i][:5]:
                syns = synonyms[i].split(" ")
                if syns[0][-1] == '=':
                    wordlist += syns[1:]
                temp += 1

    wordlist.append(word)

    return set(wordlist)

def select_ns(sentences):
    seg_list, pos_list = dataprocess.ltpprocess.ltp_process(sentences)
    fin_seg = []
    fin_pos = []
    for i in range(len(seg_list)):
        for j in range(len(seg_list[i])):
            if pos_list[i][j] == 'ns':
                fin_seg.append(seg_list[i])
                fin_pos.append(pos_list[i])
                break
    return fin_seg, fin_pos

def word_frequency(text_dict):
    """
    Count the word frequency of the input data.
    :param: dict with {id: text}
    :return: {word: appear times(int)}
    """
    word_dict = {}
    for id in text_dict:
        text = text_dict[id]
        sentences = dataprocess.ltpprocess.cut_sent(text)
        seg_list, pos_list = dataprocess.ltpprocess.ltp_process(sentences)
        for sentence in seg_list:
            for seg in sentence:
                if seg in word_dict:
                    word_dict[seg] += 1
                else:
                    word_dict.update({seg: 1})

    return word_dict

"""
text_dict = dataprocess.readdata.read_texts("train")
word_dict = word_frequency(text_dict)
np.save("../data/trainingdata/word_frequency_training.npy", word_dict)

"""


"""ns_sentences0, ns_poses0 = dataprocess.readdata.get_allns("train")
ns_sentences, ns_poses = dataprocess.readdata.get_allns("test")
ns_sentences.update(ns_sentences0)
ns_poses.update(ns_poses0)
print("S")"""

"""
triples, sentences = dataprocess.readdata.read_triple("train")
t1, t2 = dataprocess.readdata.read_triple("test")
sentences += t2
s = set()
for l in sentences:
    if l[0] != 0:
        s.add(l[0])
    if l[1] != 0:
        s.add(l[1])

sentences = list(s)
sentences = set(sentences)
ns_sentences, ns_poses = select_ns(list(sentences))

words = at_vocabulary(ns_sentences, ns_poses)
res = set(words)
"""


"""
allnegs = neg_vocabulary()
with open("../data/negatives/myallnegs.txt", 'a+') as f:
    for line in allnegs:
        f.write(line+'\n')
    f.close()
"""