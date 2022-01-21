"""
We need triple data and corresponding context data, we also need data of whole text.
For each city's data, we put it into a list, the index would be the same.
Triple:[[(),(),...](triples for entity0), [(),(),...](triples for entity1), ...]
Text:["text0", "text1", ...]
Entity:["entity0", "entity1", ...]
"""
import json
import re


textDataPath = "./data/content_list/"
tripleDataPath = "./data/tripledata/"
semanticDatapath = "./data/semantic_list/"
trainlist = []
trainentitylist = []
testlist = []
testentitylist = []
with open("./youji_train_list.txt", "r") as f:
    text = f.read()
    f.close()
    templist = text.split('\n')
    for t in templist:
        temp = t.split(' ')
        trainlist.append(temp[0])
        trainentitylist.append(temp[1])

with open("./youji_test_list.txt", "r") as f:
    text = f.read()
    f.close()
    templist = text.split('\n')
    for t in templist:
        temp = t.split(' ')
        testlist.append(temp[0])
        testentitylist.append(temp[1])


def read_triple(status):
    triples = []
    if status == "train":
        for traintriple in trainlist:
            triple = triple_jsonprocess(traintriple)
            triples.append(triple)
    else:
        for testtriple in testlist:
            triple = triple_jsonprocess(testtriple)
            triples.append(triple)

    return triples


def read_texts(status):
    """
    If data for training, input "train", else "test"
    :param status: "train" or "test"
    :return: texts, entitylist
    """

    texts = []

    if status == "train":
        for traintext in trainlist:
            text = text_jsonprocess(traintext)
            texts.append(text)

        return texts, trainentitylist

    else:
        for testtext in testlist:
            text = text_jsonprocess(testtext)
            texts.append(text)

        return texts, testentitylist


def text_jsonprocess(textnum):
    with open(textDataPath + textnum + ".json", "r") as f:
        text = f.read()
        f.close()

        # read the corresponding json data
        jsondata = json.loads(text)

        # get the text
        text = jsondata["content"]["0"]["0"]["content"]

    return text


def triple_jsonprocess(triplenum):

    triples = []

    with open(semanticDatapath + triplenum, 'r') as f:
        text = f.read()
        f.close()

        semanticData = json.loads(text)

    with open(tripleDataPath + triplenum, 'r') as f:
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

        # get the corresponding sentence from semantic data
        if j['sub_id'] != "NotFound":
            position = j['sub_id'].replace('(','').replace(')','').replace('\'', '')
            position = position.split(',')
            sentence = semanticData['"'+position[0]+'"']['"'+position[1]+'"'][int(position[2])]["source"][int(position[3])]

        if j['obj_id'] != "NotFound":
            position = j['obj_id'].replace('(', '').replace(')', '').replace('\'', '')
            position = position.split(',')
            sentence = semanticData['"' + position[0] + '"']['"' + position[1] + '"'][int(position[2])]["source"][int(position[3])]


        triples.append(triple)
    return triples
