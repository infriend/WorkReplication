import os
import json
import re
"""
Read the triples, get the relation and its synonyms, values(first entity) into the field,
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


def read_triples():
    tripleFiles = os.listdir(tripleDataPath)

    triples = []

    for i in range(len(tripleFiles)):
        with open(tripleDataPath + tripleFiles[i], 'r') as f:
            text = f.read()
            f.close()

            # read the corresponding json data
            jsondata = json.loads(text)

        for j in jsondata:
            sub_flag = re.search("地点|城市|景点", j['sub_type'])
            obj_flag = re.search("地点|城市|景点", j['obj_type'])
            if j['relation'] != 'at' or not sub_flag or not obj_flag:
                continue  # we only need 地点 or 城市 景点 at 地点 or 城市, cuz 著名景点，位置 only matches 'at' relation
            triple = (j['subject'], j['relation'], j['object'])
            triples.append(triple)

    return triples


def construct_wordfield():
    """
    Input: triples, synonyms.
    Output: word field F, a list.
    """
    F = {}

    triples = read_triples()

    for t in triples:
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
