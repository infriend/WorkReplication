import re
import os
import json

'''
split data with dot, then for each sentence, match the entity, attribute and value,
calculate the weight. each triple has one candidate sentence.
data set is organized with triples and their corresponding articles.
'''

textDataPath = "./data/contextdata/"
tripleDataPath = "./data/tripledata/"


def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")


def calc_weight(triple, s):
    relation_vocabulary = "著名景点"
    weight = 1
    # Ma
    if re.search(triple[0], s):
        weight *= 2
    # Mb
    if re.search(relation_vocabulary, s):
        weight *= 3
    else:
        weight *= 2
    # Mc
    if re.search(triple[2], s):
        weight *= 1
    else:
        weight = 0
    return weight


def choose_candidate():
    triples = []
    candidates = []

    tripleFiles = os.listdir(tripleDataPath)
    textFiles = os.listdir(textDataPath)

    for i in range(len(tripleFiles)):
        with open(textDataPath + textFiles[i], "r") as f:
            text = f.read()
            f.close()
            text = text.replace("\n", '').replace("\r", '')

            # get all the sentences
            sentences = cut_sent(text)

        with open(tripleDataPath + tripleFiles[i], 'r') as f:
            text = f.read()
            f.close()

            # read the corresponding json data
            jsondata = json.loads(text)

        # read each triple and get its related candidate sentence
        for j in jsondata:
            if j['relation'] != 'at' and (j['sub_type'] != "地点" or j['sub_type'] != "城市") and (j['obj_type'] != "地点" or j['obj_type'] != "城市"):
                continue # we only need 地点 or 城市 at 地点 or 城市, cuz 著名景点，位置 only matches 'at' relation
            triple = (j['subject'], j['relation'], j['object'])
            biggest_weight = 1
            candidate = sentences[0]

            # calculate the weight, choose the candidate sentence
            for s in sentences:
                weight = calc_weight(triple, s)
                if weight > biggest_weight:
                    biggest_weight = weight
                    candidate = s

            candidates.append(candidate)
            triples.append(triple)

    return [triples, candidates]


choose_candidate()
