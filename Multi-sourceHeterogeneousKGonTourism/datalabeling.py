import re

"""
In this module, we need to construct template files and labeling the data with BNI.
Moreover, we split word into chinese characters, labeling each character with MESB.
We need to extract < someplace at city >, 'city' and 'at' are determined by the given context,
thus any words classified as MESB would be filled in the triple as the first entity.
"""

trainingDataPath = "./data/trainingdata/"
tripleDataPath = "./data/tripledata/"


def data_labeling(triples, generators):
    # get all the attribute values
    attributes = set()
    for t in triples:
        attributes.add(t[0])
        attributes.add(t[2])

    sentences = ''
    # get the sentence
    for i in range(len(generators)):
        sentence = ''
        for w in generators[i]:
            f_flag = 0

            if w == 'f/x':
                if f_flag == 0:
                    f_flag = 1
                else:
                    f_flag = 0
                continue


            split_word = w.split("/")
            # label as b, m, e, s
            if f_flag == 1:
                word_length = len(split_word[0])
                for j in range(word_length):
                    if word_length == 1:
                        sentence += split_word[0][j] + ' ' + split_word[1] + ' ' + 'S' + '\n'
                    else:
                        if j == 0:
                            sentence += split_word[0][j] + ' ' + split_word[1] + ' ' + 'B' + '\n'
                        elif j == word_length-1:
                            sentence += split_word[0][j] + ' ' + split_word[1] + ' ' + 'E' + '\n'
                        else:
                            sentence += split_word[0][j] + ' ' + split_word[1] + ' ' + 'M' + '\n'
            # label as n
            else:
                for c in split_word[0]:
                    word_length = len(split_word[0])
                    for j in range(word_length):
                        sentence += split_word[0][j] + ' ' + split_word[1] + ' ' + 'N' + '\n'
        sentences += sentence
        sentences += '\n'

    return sentences


def template_generator():
    print("aa")
