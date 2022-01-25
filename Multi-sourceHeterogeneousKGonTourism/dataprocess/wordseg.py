import jieba
import jieba.posseg

"""
Chinese word segmentation, along with part of speech labeling
"""


def word_segmentation(candidates):
    generators = []
    result = []
    for c in candidates:
        r = jieba.posseg.cut(c)
        generators.append(r)
    for g in generators:
        templist = []
        for w in g:
            templist.append(w)
        result.append(templist)

    return result  # return word generators


'''
temp = candidate.choose_candidate()
word_generators = word_segmentation(temp[1])
'''
