"""
training input: json triples and text
input: text data
output: get the current site name, we extract the place info and famous sites info with CRFPP,
we only extract the 'at' relation, thus we extract the subject
"""
import dataprocess.readdata
import dataprocess.wordseg
import dataprocess.datalabeling
import dataprocess.candidate
import crfpp


def test():
    texts, testentitydict = dataprocess.readdata.read_texts("test")
    test_text = ''

    # for each text we have one test data
    for i in list(texts):
        sentences = dataprocess.candidate.cut_sent(texts[i])
        generators = dataprocess.wordseg.word_segmentation(sentences)
        for j in range(len(generators)):
            sentence = ''
            for w in generators[j]:
                split_word = [w.word, w.flag]
                for c in split_word[0]:
                    sentence += c + ' ' + split_word[1] + '\n'
            test_text += sentence
            test_text += '\n'

    with open("./data/testdata/test.txt", 'a+') as f:
        f.write(test_text)
        f.close()

    test_res = crfpp.crftest()

    with open("./data/testdata/test.res", 'a') as f:
        f.write(test_res)
        f.close()


if __name__ == '__main__':
    test()

