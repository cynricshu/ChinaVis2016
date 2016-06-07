import os
import LineData
import re
import numpy as np
import lda
import lda.datasets
import nltk
import util.ldaHelper as ldaHelper
import util.helper as helper
import util.fileHelper as fileHelper


def firstLoop(line, tuple):
    subjectdict = tuple[0]
    data = LineData.LineData(line)
    subject = data.getSubject().strip()

    for word in helper.keywords:
        subject = subject.replace(word, "")
    subject = subject.strip()
    if subject != "":
        if subject in subjectdict:
            subjectdict[subject] += 1
        else:
            subjectdict[subject] = 1


def handleOriginFile(func, outputFile):
    """
    :return:
    """
    dataDir = "data/After2"
    subjectdict = dict()

    fileList = os.listdir(dataDir)
    for filename in fileList:
        fileHelper.readCsv(dataDir + "/" + filename, func, subjectdict)
        print("%s execute ok" % filename)

    print(len(subjectdict))
    fileHelper.writeDictToFile(outputFile, subjectdict)
    return subjectdict


def handleSubject1(outputFile):
    """
    :return: dict
    """
    index = 0
    termdict = dict()
    subjectList = list()

    f = open("data/topic/subject1_w.txt")
    for item in f:
        count = item[0: item.index(":")]
        subject = item[item.index(":") + 1: len(item)].strip()

        for (regex, repl) in helper.regexList.items():
            subject = regex.sub(repl, subject)
        for s in helper.specialSet:
            subject = subject.replace(s, "")

        termList = nltk.regexp_tokenize(subject, helper.nltkPattern)  # use nltk-package to participle the subject
        s = ""
        for term in termList:
            if term.lower() not in helper.excludeSet:
                s += term + " "  # reconstruct the subject
                if term not in termdict:
                    termdict[term.strip()] = index
                    index += 1

        if s != "":
            regex = re.compile("\s+")
            s = regex.sub(" ", s)
            subjectList.append("{}:{}".format(count, s.strip()))

    fileHelper.writeIterableToFile(outputFile, subjectList)
    return termdict


def getTermFromFile():
    """
    :return:
    """
    termdict = dict()
    index = 0
    f = open("data/topic/subject2_w.txt")
    for subject in f:
        subject = subject[subject.index(":") + 1: len(subject)].strip()
        termList = subject.split(" ")
        for term in termList:
            if term not in termdict:
                termdict[term.strip()] = index
                index += 1
    return termdict


def testRegex():
    # a = "[!EYS-874-87004]: Assignment - Installazione su disposito Osx iMac"
    # b = "Assignment - Installazione su disposito Osx iMac"
    # regex = re.compile("\[.*\]: ")
    # print(regex.sub("", a))
    # print(regex.sub("", b))
    regex = re.compile("the")
    subject = "Strange sign on the thetarget".strip()
    subject = regex.sub(" ", subject)
    print(subject)


def ldaTest():
    X = ldaHelper.load_reuters()
    vocab = ldaHelper.load_reuters_vocab()
    titles = ldaHelper.load_reuters_titles()
    n_top_words = 15

    X.shape
    X.sum()
    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    print("lda start to fit")
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works

    print("start to write file")
    f = open("data/output/ldaResult_w.txt", "w")
    f.write("ntopics=20, n_iter=1500, random_state=1\n")
    f.write("n_top_words={}\n\n\n".format(n_top_words))

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
        f.write('Topic {}: {}\n'.format(i, ' '.join(topic_words)))

    doc_topic = model.doc_topic_
    for i in range(len(titles)):
        if i % 1000 == 0:
            f.flush()
        f.write("{}:{}\n".format(i, doc_topic[i].argmax()))
    f.close()


def nltkTest():
    s = "russia licenza 8.1.5 U.S."
    res = nltk.regexp_tokenize(s, helper.nltkPattern)
    print(res)

    s = "Saldo vs. Fattura n. 2015/004"
    res = nltk.regexp_tokenize(s, helper.nltkPattern)
    print(res)


def genLdaInputDoc(termdict):
    if termdict is None or len(termdict) == 0:
        termdict = getTermFromFile()  # {term1: index1, term2: index2 ... }
    outlist = list()

    f = open("data/topic/subject2_w.txt")
    for line in f:
        count = int(line[0: line.index(":")])
        line = line[line.index(":") + 1: len(line)].strip()
        temp = dict()  # {index of term: count} we use it to save the count of each term(use index to represent a term)
        terms = line.split(" ")
        for term in terms:
            index = termdict[term]
            if index in temp:
                temp[index] += 1
            else:
                temp[index] = 1
        formattedStr = str(len(temp))
        keyList = list(temp.keys())
        keyList.sort()

        for i in range(len(keyList)):
            formattedStr += " %s:%s" % (str(keyList[i]), str(count * temp[keyList[i]]))
        outlist.append(formattedStr.strip())

    reversedTermDict = dict()
    for term, index in termdict.items():
        reversedTermDict[index] = term

    outfile = "data/topic/subject2_w.tokens"
    fileHelper.writeIterableToFileWithIndex(outfile, reversedTermDict)

    outfile = "data/topic/subject2_w.ldac"
    fileHelper.writeIterableToFileWithIndex(outfile, outlist)


def main():
    # subjectdict = handleOriginFile(firstLoop, "data/topic/subject1_w.txt")

    # termdict = handleSubject1("data/topic/subject2_w.txt")
    # genLdaInputDoc(None)
    ldaTest()
    # nltkTest()
    # testRegex()

    print("over")


if __name__ == '__main__':
    main()
