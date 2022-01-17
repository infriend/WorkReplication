from ltp import LTP
import re
import os

"""
First, sentence segmentation. Then for each sentence, we do word segmentation.
Then we label the part of speech.
"""

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


def get_segmentedsentences():
    textFiles = os.listdir(textDataPath)

    sentences = []

    for i in range(len(textFiles)):
        with open(textDataPath + textFiles[i], "r") as f:
            text = f.read()
            f.close()
            text = text.replace("\n", '').replace("\r", '')

            # get all the sentences
            sentences = cut_sent(text)

    return sentences


def ltp_process(sentences):
    ltp = LTP()

    seg_list = []
    pos_list = []

    for s in sentences:
        seg, hidden = ltp.seg([s])
        pos = ltp.pos(hidden)
        seg_list.append(seg)
        pos_list.append(pos)

    return seg_list, pos_list


print("aa")

