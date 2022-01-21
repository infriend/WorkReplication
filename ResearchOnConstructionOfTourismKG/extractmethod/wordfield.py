from dataprocess import readdata
import re
"""
Read the triples, put the relation and its synonyms, values(first entity) into the field,
values have special ways to calculate weight.
"""

tripleDataPath = "./data/tripledata/"
synonymsPath = ''  # TODO: confirm the usage of the synonyms by LTP

C_standard = 4
W_standard = 2


def is_chinese(ch):
    if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def construct_wordfield():
    """
    Input: triples, synonyms.
    Output: word field F, a list.
    """
    F = {}

    triples = readdata.read_triple()

    for city in triples:
        for t in city:
            if t[0] not in F:
                if re.search("[0-9]", t[0]):
                    F.update({t[0], 0.5})
                elif len(t[0]) == 1 and is_chinese(t[0]):
                    F.update({t[0], 1})
                else:
                    F.update({t[0], 2})

    with open(synonymsPath, 'r') as f:
        text = f.read()
        f.close()
        synonyms = text.split('\n')  # Temporarily, we take synonyms as a file with one word in one line.

    for word in synonyms:
        F.update({word, 3})  # We set all the attribute trigger words in the synonym file.

    return F


def extract_field(field, seg_list, pos_list, entity):
    """
    Extract attribute value from sentences, these sentences should have same subject.
    :param field: word field
    :param seg_list: segments from sentences, which was segmented by ltp.
    :param pos_list: pos of the sentences
    :param entity: the subject
    :return: extracted value
    """
    ca = []
    ca_pos = []

    triples = []

    for i in range(len(seg_list)):
        ta = []
        for w in seg_list[i]:
            if w in field:
                ta.append(field[w])
        c = len(ta)
        w = sum(ta)/c
        if c >= C_standard and w >= W_standard:
            ca.append(seg_list[i])
            ca_pos.append(pos_list[i])

    for i in range(len(ca_pos)):
        for j in range(len(ca_pos[i])):
            if ca_pos[i][j] == 'ns' or ca_pos[i][j] == 'n':
                triples.append(set(ca[i][j], 'at', entity))

    return triples
