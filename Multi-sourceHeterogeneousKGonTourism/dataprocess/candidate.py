import re
import os
import json
import dataprocess.readdata
'''
split data with dot, then for each sentence, match the entity, attribute and value,
calculate the weight. each triple has one candidate sentence.
data set is organized with triples and their corresponding articles.
'''

textDataPath = "./data/contextdata/"
tripleDataPath = "./data/tripledata/"

# sentence segmentation
def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")


def merge_intervals(intervals):

    intervals.sort(key=lambda x: x[0])

    merged = []
    for interval in intervals:
        # 如果列表为空，或者当前区间与上一区间不重合，直接添加
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            # 否则的话，我们就可以与上一区间进行合并
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged


# In our 'at' relation, the first entity is object, the second one is subject.
def calc_weight(triple, s):
    relation_vocabulary = "景点|位置|位于|在|位在"
    weight = 1

    intersection = []

    # Ma
    ma = re.search(triple[2], s)
    mb = re.search(relation_vocabulary, s)
    mc = re.search(triple[0], s)

    if ma:
        weight *= 2

    # Mb
    if mb:
        weight *= 3
    else:
        weight *= 2

    # Mc
    if mc:
        weight *= 1
    else:
        weight *= 0

    return [weight, s]


def choose_candidate():
    tripleRes = []
    candidatesRes = []

    trainlist = []
    with open("../data/youji_train_list.txt", "r") as f:
        text = f.read()
        f.close()
        templist = text.split('\n')
        for t in templist:
            trainlist.append(t)

    text_dict = dataprocess.readdata.read_texts("train")
    tripledict = dataprocess.readdata.read_triple("train")

    # for every text
    for k in text_dict:

        text = text_dict[k]

        # get all the sentences
        sentences = cut_sent(text)

        ts = tripledict[k]  # corresponding triples
        attributes = set()  # all attributes in the triples
        candidates = []  # save all the candidates

        # read each triple and get its related candidate sentence
        for j in ts:
            # get all the attribute values
            attributes.add(j[0])
            attributes.add(j[2])

            biggest_weight = 1
            candidate = sentences[0]

            # calculate the weight, choose the candidate sentence
            for s in sentences:
                res = calc_weight(j, s)
                weight = res[0]
                s = res[1]
                if weight > biggest_weight:
                    biggest_weight = weight
                    candidate = s

            candidates.append(candidate)  # all candidates in one text
            tripleRes.append(j)

        # remove duplicate candidate, label all the entities in the candidates
        candidates = set(candidates)

        # for one sentence
        for candidate in candidates:
            intersection = []

            for attr in attributes:
                ma_gen = re.finditer(attr, candidate)

                try:
                    ma = next(ma_gen)
                except StopIteration:
                    pass
                else:
                    span = [ma.span()[0], ma.span()[1]]
                    intersection.append(span)
                    for ma in ma_gen:
                        span = [ma.span()[0], ma.span()[1]]
                        intersection.append(span)

                mc_gen = re.finditer(attr, candidate)

                try:
                    mc = next(mc_gen)
                except StopIteration:
                    pass
                else:
                    span = [mc.span()[0], mc.span()[1]]
                    intersection.append(span)
                    for mc in mc_gen:
                        span = [mc.span()[0], mc.span()[1]]
                        intersection.append(span)

            intersection = merge_intervals(intersection)
            drift = 0
            for i in intersection:
                candidate = candidate[:i[0] + drift] + '↑' + candidate[i[0] + drift:i[1] + drift] + '↑' + candidate[i[1] + drift:]
                drift += 2
            candidatesRes.append(candidate)

    return tripleRes, candidatesRes

