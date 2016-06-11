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
import json

delimer = "DELIMER"


def firstLoop(line, tuple):
    subjectdict = tuple[0]
    data = LineData.LineData(line)
    subject = data.getSubject().strip()

    for word in helper.keywords:
        subject = subject.replace(word, "")
    subject = subject.strip()
    if subject != "":
        if subject in subjectdict:
            subjectdict[subject][0] += 1
        else:
            subjectdict[subject] = [1, data.getDateSent(), data.getDateReceive()]


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
    fileHelper.writeDictToFile(outputFile, subjectdict,
                               lambda key, val: "{}DELIMER{}DELIMER{}DELIMER{}\n".format(val[0], val[1], val[2], key))
    return subjectdict


def handleSubject1(outputFile):
    """
    :return: dict
    """
    index = 0
    termdict = dict()
    subjectList = list()

    f = open("data/topic/subject1_w_date.txt")
    for item in f:
        array = item.strip().split("DELIMER")
        count = array[0]
        subject = array[3]

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
            subjectList.append("{}DELIMER{}DELIMER{}DELIMER{}".format(count, array[1], array[2], s.strip()))

    fileHelper.writeIterableToFile(outputFile, subjectList)
    return termdict


def findSubjectByCategory():
    f = open("data/topic/weight/subject1_w.txt")
    alarm_pattern = re.compile("\[!.*\].*")
    bulk_pattern = re.compile("\[BULK\].*")
    index = 0

    advArray = []
    advdict = {'name': 'Advertisement mail', 'children': advArray, 'value': 165}
    alarmArray = []
    alarmdict = {'name': 'Alarm mail', 'children': alarmArray, 'value': 7237}
    bulkArray = []
    bulkdict = {'name': 'Bulk mail', 'children': bulkArray, 'value': 2664}
    meetingArray = []
    meetingdict = {'name': 'Meeting mail', 'children': meetingArray, 'value': 1863}
    travelArray = []
    traveldict = {'name': 'Travel mail', 'children': travelArray, 'value': 1433}

    for item in f:
        array = item.strip().split(":")
        count = array[0]
        subject = ''.join(array[1:]).strip()

        if "<adv>" in subject.lower() or "(adv)" in subject.lower():
            advArray.append({'id': index, 'value': count, 'name': subject})

        if re.match(alarm_pattern, subject):
            alarmArray.append({'id': index, 'value': count, 'name': subject})

        if re.match(bulk_pattern, subject):
            bulkArray.append({'id': index, 'value': count, 'name': subject})

        if "travel" in subject.lower() or "hotel" in subject.lower() or "tour" in subject.lower() \
                or "journey" in subject.lower() or "trip" in subject.lower():
            travelArray.append({'id': index, 'value': count, 'name': subject})

        if "meeting" in subject.lower() or "conference" in subject.lower() or "forum" in subject.lower():
            meetingArray.append({'id': index, 'value': count, 'name': subject})

        index += 1

    print("adv mail:{}, alarm mail:{}, bulk mail:{}, meeting mail: {}, travel mail:{}".format(
        str(len(advArray)), str(len(alarmArray)), str(len(bulkArray)), str(len(travelArray)), str(len(meetingArray))
    ))

    alldict = {'name': 'All Mail', 'children': [advdict, alarmdict, bulkdict, meetingdict, traveldict]}
    with open("data/output/category.json", "w") as outfile:
        json.dump(alldict, outfile)


def getTermFromFile():
    """
    :return:
    """
    termdict = dict()
    index = 0
    f = open("data/topic/subject2_w_date.txt")
    for line in f:
        array = line.strip().split(delimer)
        subject = array[3].strip()
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
    model = lda.LDA(n_topics=100, n_iter=1500, random_state=1)
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

    f = open("data/topic/subject2_w_date.txt")
    for line in f:
        array = line.strip().split(delimer)
        count = array[0]
        line = array[3].strip()
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

    outfile = "data/topic/subject2_w_date.tokens"
    fileHelper.writeIterableToFileWithIndex(outfile, reversedTermDict)

    outfile = "data/topic/subject2_w_date.ldac"
    fileHelper.writeIterableToFileWithIndex(outfile, outlist)


def main():
    # subjectdict = handleOriginFile(firstLoop, "data/topic/subject1_w_date.txt")

    # termdict = handleSubject1("data/topic/subject2_w_date.txt")
    # genLdaInputDoc(None)
    # ldaTest()
    # nltkTest()
    # testRegex()
    findSubjectByCategory()

    print("over")


if __name__ == '__main__':
    main()
