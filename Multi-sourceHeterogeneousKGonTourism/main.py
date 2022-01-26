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

    values = set()
    relations = set()
    word = ''
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

        test_res = crfpp.crftest()

        for line in test_res:
            if line == '\n':
                continue
            if line[-2] == 'S':
                values.add(line[0] + '\n')
                relations.add(line[0] + ' ' + 'at' + ' ' + testentitydict[i] + '\n')
            elif line[-2] == 'B' or line[-2] == 'M':
                word += line[0]
            elif line[-2] == 'E':
                word += line[0]
                values.add(word + '\n')
                relations.add(word + ' ' + 'at' + ' ' + testentitydict[i] + '\n')
                word = ''
            else:
                pass

        print(testentitydict[i])

    with open("./data/testdata/entity.txt", 'a+') as f:
        for every in iter(values):
            f.write(every)
        f.close()

    with open("./data/testdata/relation.txt", 'a+') as f:
        for every in iter(relations):
            f.write(every)
        f.close()

"""
    with open("./data/testdata/test.txt", 'a+') as f:
        f.write(test_text)
        f.close()

    test_res = crfpp.crftest()
    with open("./data/testdata/test_res.txt", 'a') as f:
        for string in test_res:
            f.write(string)
        f.close()
"""

if __name__ == '__main__':
    test()
