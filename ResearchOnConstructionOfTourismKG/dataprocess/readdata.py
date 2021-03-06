"""
We need triple data and corresponding context data, we also need data of whole text.
For each city's data, we put it into a list, the index would be the same.
Triple:[[(),(),...](triples for entity0), [(),(),...](triples for entity1), ...]
Text:["text0", "text1", ...]
Entity:["entity0", "entity1", ...]
"""
import json
import re
import dataprocess.ltpprocess

textDataPath = "./data/content_list/"
semanticDatapath = "./data/semantic_list/"
trainDataPath = "./data/trainingdata/"
trainlist = []
trainentitylist = []
testlist = []
testentitylist = []
testentitydict = {}
with open("./data/youji_train_list.txt", "r") as f:
    text = f.read()
    f.close()
    templist = text.split('\n')
    for t in templist:
        trainlist.append(t)

with open("./data/youji_test_list.txt", "r") as f:
    text = f.read()
    f.close()
    templist = text.split('\n')
    for t in templist:
        temp = t.split(' ')
        testlist.append(temp[0])
        testentitylist.append(temp[1])
        testentitydict.update({temp[0]: temp[1]})


def read_triple(status):
    if status == "train":
        # get train dict, {id: [triples]}
        triples, sentences = triple_jsonprocess("train")

    else:
        # get test dict
        triples, sentences = triple_jsonprocess("test")

    return triples, sentences


def read_texts(status):
    """
    If data for training, input "train", else "test"
    :param status: "train" or "test"
    :return: texts, a dict with {id: text}, entitylist {id: entity}
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

        return texts, testentitydict


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
    Get all the triples and their corresponding sentence at the same time.
    :return triples, sentences:
    """
    tripledict = {}
    sentencedict = {}

    textid = ""

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

    num = 0
    # for each triple data
    for j in jsondata:
        # read text
        if textid != j["id"]:
            textid = j["id"]
            print("Read Triple Text %d %d" % (textid, num))
            with open(semanticDatapath + str(textid) + ".json", 'r') as f:
                text = f.read()
                f.close()
                semanticData = json.loads(text)
            tripledict.update({textid: []})
            sentencedict.update({textid: []})

        # we only need ?????? or ?????? ?????? at ?????? or ??????, cuz ????????????????????? only matches 'at' relation
        sub_flag = re.search("??????|??????|??????", j['sub_type'])
        obj_flag = re.search("??????|??????|??????", j['obj_type'])
        if j['relation'] != 'at' or not sub_flag or not obj_flag:
            continue

        # get the triple tuple
        triple = (j['subject'], j['relation'], j['object'])

        tempsentence = [0, 0]

        # get the corresponding sentence from semantic data
        if j['sub_id'] != "NotFound":
            position = j['sub_id'].replace('(', '').replace(')', '').replace('\'', '')
            position = position.split(',')
            sentence0 = semanticData[str(position[0])][str(position[1])][int(position[2])]["source"][
                int(position[3])]
            tempsentence[0] = sentence0

        if j['obj_id'] != "NotFound":
            position = j['obj_id'].replace('(', '').replace(')', '').replace('\'', '')
            position = position.split(',')
            sentence1 = semanticData[str(position[0])][str(position[1])][int(position[2])]["source"][
                int(position[3])]
            tempsentence[1] = sentence1

        # with the same index
        sentencedict[textid].append(tempsentence)
        tripledict[textid].append(triple)

    return tripledict, sentencedict


def get_allns(status):
    if status == 'train':
        texts = read_texts(status)
    else:
        texts, testentities = read_texts(status)
    ns_sentences = {}
    ns_poses = {}
    for id in texts:
        print("Get all ns: text %s" % id)
        selected_sentences = []
        selected_poses = []
        text = texts[id]
        sentences = dataprocess.ltpprocess.cut_sent(text)
        print("Sentence number: %d" %(len(sentences)))
        seg_list, pos_list = dataprocess.ltpprocess.ltp_process(sentences)
        # for each sentence
        for i in range(len(seg_list)):

            # for each word's pos
            for j in range(len(seg_list[i])):
                if pos_list[i][j] == 'ns':
                    selected_sentences.append(seg_list[i])
                    selected_poses.append(pos_list[i])
                    break
        ns_sentences.update({id: selected_sentences})
        ns_poses.update({id: selected_poses})

    return ns_sentences, ns_poses