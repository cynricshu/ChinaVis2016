import helper
import csv
import codecs
import os
import LineData
import sys
import re
import numpy as np
import lda
import lda.datasets
import nltk
import ldaHelper


def handleOriginFile():
    """
    :return:
    """
    dataDir = "data/After2"
    toOut = "data/topic/subject1.txt"
    subjectSet = set()

    csv.field_size_limit(sys.maxsize)
    fileList = os.listdir(dataDir)
    for filename in fileList:
        f = csv.reader(codecs.open(dataDir + "/" + filename, "r", "iso-8859-1"))
        header = f.__next__()

        for line in f:
            if len(line) > 1:
                data = LineData.LineData(line)
                subject = data.getSubject().strip()

                for word in helper.keywords:
                    subject = subject.replace(word, "")
                subjectSet.add(subject.strip())
        print("%s execute ok" % filename)

    print(len(subjectSet))

    count = 0
    f = open(toOut, "w")
    for name in subjectSet:
        f.write(name + "\n")
        count += 1
        if count % 500 == 0:
            f.flush()
    f.close()


def handleSubject1():
    """
    :return: dict
    """
    index = 0
    termdict = dict()
    subjectSet = list()
    toOut = "data/topic/subject2.txt"

    f = open("data/topic/subject1.txt")
    for subject in f:
        subject = subject.strip()

        for (regex, repl) in helper.regexList.items():
            subject = regex.sub(repl, subject)
        for str in helper.specialSet:
            subject = subject.replace(str, "")

        subject = nltk.regexp_tokenize(subject, helper.nltkPattern)
        str = ""
        for term in subject:
            if term.lower() not in helper.excludeSet:
                str += term + " "
                if term not in termdict:
                    termdict[term.strip()] = index
                    index += 1

        if str != "":
            regex = re.compile("\s+")
            str = regex.sub(" ", str)
            subjectSet.append(str.strip())

    count = 0
    f = open(toOut, "w")
    for subject in subjectSet:
        f.write(subject + "\n")
        count += 1
        if count % 500 == 0:
            f.flush()
    f.close()
    return termdict


def getTerm():
    """
    :return:
    """
    termdict = dict()
    index = 0
    f = open("data/topic/subject2.txt")
    for subject in f:
        subject = subject.strip()
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

    X.shape
    X.sum()
    model = lda.LDA(n_topics=20, n_iter=3000, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 12
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    doc_topic = model.doc_topic_
    for i in range(20):
        print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))


def nltkTest():
    s = "russia licenza 8.1.5 U.S."
    res = nltk.regexp_tokenize(s, helper.nltkPattern)
    print(res)

    s = "Saldo vs. Fattura n. 2015/004"
    res = nltk.regexp_tokenize(s, helper.nltkPattern)
    print(res)


def genLdaInputDoc(termdict):
    if len(termdict) == 0:
        termdict = getTerm()  # {term1: index1, term2: index2 ... }
    f = open("data/topic/subject2.txt")
    outlist = list()
    for line in f:
        line = line.strip()
        temp = dict()  # {index: count}
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
            formattedStr += " %s:%s" % (str(keyList[i]), str(temp[keyList[i]]))
        outlist.append(formattedStr.strip())

    reversedTermDict = dict()
    for term, index in termdict.items():
        reversedTermDict[index] = term

    outfile = "data/topic/subject2.tokens"
    count = 0
    f = open(outfile, "w")
    for i in range(len(reversedTermDict)):
        f.write(reversedTermDict[i] + "\n")
        count += 1
        if count % 500 == 0:
            f.flush()
    f.close()

    outfile = "data/topic/subject2.ldac"
    count = 0
    f = open(outfile, "w")
    for i in range(len(outlist)):
        f.write(outlist[i] + "\n")
        count += 1
        if count % 500 == 0:
            f.flush()
    f.close()


def main():
    # handleOriginFile()
    # termdict = handleSubject1()
    # genLdaInputDoc(termdict)
    ldaTest()
    # nltkTest()
    # testRegex()

    print("over")


if __name__ == '__main__':
    main()
