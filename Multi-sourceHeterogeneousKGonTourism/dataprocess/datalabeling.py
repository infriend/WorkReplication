import re
"""import wordseg
import candidate"""

"""
In this module, we need to construct template files and labeling the data with BNI.
Moreover, we split word into chinese characters, labeling each character with MESB.
We need to extract < someplace at city >, 'city' and 'at' are determined by the given context,
thus any words classified as MESB would be filled in the triple as the first entity.
"""

trainingDataPath = "./data/trainingdata/"
tripleDataPath = "./data/tripledata/"


def data_labeling(generators):
    sentences = ''
    # get the sentence
    for i in range(len(generators)):
        sentence = ''
        f_flag = 0
        for w in generators[i]:
            if w.word == '↑':
                if f_flag == 0:
                    f_flag = 1
                else:
                    f_flag = 0
                continue

            split_word = [w.word, w.flag]
            # label as b, m, e, s
            if f_flag == 1:
                word_length = len(split_word[0])
                for j in range(word_length):
                    if word_length == 1:
                        sentence += split_word[0][j] + ' ' + split_word[1] + ' ' + 'S' + '\n'
                    else:
                        if j == 0:
                            sentence += split_word[0][j] + ' ' + split_word[1] + ' ' + 'B' + '\n'
                        elif j == word_length - 1:
                            sentence += split_word[0][j] + ' ' + split_word[1] + ' ' + 'E' + '\n'
                        else:
                            sentence += split_word[0][j] + ' ' + split_word[1] + ' ' + 'M' + '\n'
            # label as n
            else:
                for c in split_word[0]:
                    sentence += c + ' ' + split_word[1] + ' ' + 'N' + '\n'

        sentences += sentence
        sentences += '\n'

    return sentences


"""triples, candidates = candidate.choose_candidate()
generators = wordseg.word_segmentation(candidates)
sentences = data_labeling(triples, generators)
with open("../data/trainingdata/train.txt", 'a') as f:
    f.write(sentences)
    f.close()"""