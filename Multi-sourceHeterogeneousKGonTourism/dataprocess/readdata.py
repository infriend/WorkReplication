"""
We need triple data and corresponding context data, we also need data of whole text.
For each city's data, we put it into a list, the index would be the same.
Triple:[[(),(),...](triples for entity0), [(),(),...](triples for entity1), ...]
Text:["text0", "text1", ...]
Entity:["entity0", "entity1", ...]
"""
import os
import json
import re

textDataPath = "./data/content_list/"
semanticDatapath = "./data/semantic_list/"
trainDataPath = "./data/trainingdata/"
trainlist = []
trainentitylist = []
testlist = []
testentitylist = []
traintripledict = {}
testtripledict = {}
print(os.getcwd())
with open("./data/youji_train_list.txt", "r") as f:
    text = f.read()
    f.close()
    templist = text.split('\n')
    for t in templist:
        trainlist.append(t)
        traintripledict.update({t: []})

with open("./data/youji_test_list.txt", "r") as f:
    text = f.read()
    f.close()
    templist = text.split('\n')
    for t in templist:
        temp = t.split(' ')
        testlist.append(temp[0])
        testentitylist.append(temp[1])
        testtripledict.update({t: []})


def read_triple(status):
    triples = []
    if status == "train":
        # get train dict, {id: [triples]}
        triples = triple_jsonprocess("train")

    else:
        # get test dict
        triples = triple_jsonprocess("test")

    return triples


def read_texts(status):
    """
    If data for training, input "train", else "test"
    :param status: "train" or "test"
    :return: texts, entitylist
    """

    texts = {}

    if status == "train":
        for traintext in trainlist:
            text = text_jsonprocess(traintext)
            texts.update({traintext: text})

        return texts

    else:
        for testtext in testlist:
            text = text_jsonprocess(testtext)
            texts.update({testtext: text})

        return texts, testentitylist


def text_jsonprocess(textnum):
    """
    Read one text data from json
    :param textnum: the text number
    :return: corresponding text
    """
    with open(textDataPath + textnum + ".json", "r") as f:
        text = f.read()
        f.close()

        # read the corresponding json data
        jsondata = json.loads(text)

        text = ""

        # get the text
        for dic in jsondata['content']["0"]["0"]:
            text += dic['content']

    return text


def triple_jsonprocess(status):
    """
    Read triples first, then read the text from id, if id is different from the next triple, read new text.
    :return:
    """
    global traintripledict
    global testtripledict

    if status == "train":
        with open("./data/trainingdata/youji_train" + ".json", "r") as f:
            text = f.read()
            f.close()

            # read the corresponding json data
            jsondata = json.loads(text)
    else:
        with open("./data/testdata/youji_test" + ".json", "r") as f:
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
        textid = j["id"]
        if status == "train":
            traintripledict[str(textid)].append(triple)
        else:
            testtripledict[str(textid)].append(triple)

    if status == "train":
        return traintripledict
    else:
        return testtripledict
