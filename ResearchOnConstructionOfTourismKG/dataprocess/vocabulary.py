"""
Search all the at relation's corresponding sentence，get its v, v+p, then identify its effectiveness by hand.
Search all the synonyms of the words above.

For negative words, first handmade a small vocabulary, then use synonyms to expand it.

We only use =.
"""
import re
import dataprocess.ltpprocess

negativewords_sample = []
with open("../data/dict_negative.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        negativewords_sample.append(line.split('\t')[0])
    f.close()

synonyms = []
synonymPath = '../data/synonyms.txt'
with open(synonymPath, 'r') as f:
    lines = f.readlines()
    for line in lines:
        synonyms.append(line)
    f.close()


# input all the at relation sentence, use ltp to seg, pos with v or v+p
def at_vocabulary(sentences):
    """
    Input all the at relation sentences, out put word list.
    :param sentences: at relation sentences
    :return: at relation's trigger word list
    """
    seg_list, pos_list = dataprocess.ltpprocess.ltp_process(sentences)
    triggerwords = []
    wordres = []

    # for each sentence
    for i in range(len(seg_list)):
        # for each word
        for j in range(len(i)):
            if pos_list[i][j] == 'v':
                if j < len(i)-1:
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
        wordres += syns

    res = set(wordres)

    return res


def neg_vocabulary():
    res = []
    for neg in negativewords_sample:
        syns = search_syn(neg)

    return res


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
                syns = synonyms[i].split(" ")
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
