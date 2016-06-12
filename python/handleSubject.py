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
import codecs
from bson import json_util

delimer = "DELIMER"


def firstLoop(line, lineNum, tuple):
    # print("firstLoop: {}".format(lineNum))
    if len(line) != 15:
        return
    data = LineData.LineData(line)
    datesent = helper.datetimeFromStr(lineNum, data.getDateSent(), helper.datetimeFullFormat)
    daterecv = helper.datetimeFromStr(lineNum, data.getDateReceive(), helper.datetimeFullFormat)

    if datesent is None or daterecv is None:
        return

    # if lineNum == 24419:
    #     print(line)
    #     print(data)
    #     print(data.getDateSent())
    #     print(data.getDateReceive())

    subjectdict = tuple[0]
    subject = data.getSubject().strip()

    for word in helper.keywords:
        subject = subject.replace(word, "").strip()  # remove some meaningless words
    if subject != "":

        if subject in subjectdict:
            subjectdict[subject]['count'] += 1
            subjectdict[subject]['importance'] += data.getImportance()
            if subjectdict[subject]['min_datesent'] > datesent:
                subjectdict[subject]['min_datesent'] = datesent
            if subjectdict[subject]['min_daterecv'] > daterecv:
                subjectdict[subject]['min_daterecv'] = daterecv

            if subjectdict[subject]['max_datesent'] < datesent:
                subjectdict[subject]['max_datesent'] = datesent
            if subjectdict[subject]['max_daterecv'] < daterecv:
                subjectdict[subject]['max_daterecv'] = daterecv

        else:
            subjectdict[subject] = {'count': 1, 'min_datesent': datesent, 'max_datesent': datesent,
                                    'min_daterecv': daterecv, 'max_daterecv': daterecv,
                                    'importance': data.getImportance()}


def handleOriginFile(outputFile):
    """
    :return:
    """
    dataDir = "data/After2"
    subjectdict = dict()

    fileList = os.listdir(dataDir)
    for filename in fileList:
        fileHelper.readCsv(dataDir + "/" + filename, firstLoop, subjectdict)
        print("%s execute ok" % filename)
        # break

    print(len(subjectdict))
    # fileHelper.writeDictToFile(outputFile, subjectdict,
    #                            lambda key, val: "{}DELIMER{}DELIMER{}DELIMER{}\n".format(val[0], val[1], val[2], key))
    # with open("data/topic/weight/subject1_w.txt") as f:
    with open("data/topic/weight&date/subject1_w_date.txt", "w") as outfile:
        for subject in subjectdict:
            count = subjectdict[subject]['count']
            min_datesent = subjectdict[subject]['min_datesent']
            min_daterecv = subjectdict[subject]['min_daterecv']
            max_datesent = subjectdict[subject]['max_datesent']
            max_daterecv = subjectdict[subject]['max_daterecv']
            importance = subjectdict[subject]['importance']
            outfile.write(
                "{},{},{},{},{},{},{}\n".format(count, subject, min_datesent, max_datesent, min_daterecv,
                                                max_daterecv, importance))
            # json.dump(subjectdict, outfile, default=json_util.default)
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
    f = open("data/output/ldaResult_topic-doc_w.txt", "w")
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


def resort(file1, file2):
    """
    将file2里面的数据按照file1里面的顺序,重新排序
    :param file1:
    :param file2:
    :return:
    """
    subjectdict = dict()
    # 读一遍file2,将数据先存到字典中
    with open(file2) as file2:
        for line in file2:
            array = line.strip().split(",")
            count = array[0]
            subject = array[1]
            min_datesent = array[2]
            max_datesent = array[3]
            min_daterecv = array[4]
            max_daterecv = array[5]
            importance = array[6]

            subjectdict[subject] = {'count': count, 'min_datesent': min_datesent, 'max_datesent': max_datesent,
                                    'min_daterecv': min_daterecv, 'max_daterecv': max_daterecv,
                                    'importance': importance}
    print(len(subjectdict))

    error_count = 0
    index = 0
    with open(file1) as file1:
        with open("data/topic/weight&date/subject_1_date_sorted.txt", "w") as outfile:
            for line in file1:
                count = line[0: line.index(":")]
                subject = line[line.index(":") + 1: len(line)].strip()
                if subject in subjectdict:
                    # dcount = subjectdict[subject]['count']
                    # if count != dcount:
                    #     print("error! not match, subject:{}, origin count:{}, new count:{}".format(subject, count, dcount))
                    min_datesent = subjectdict[subject]['min_datesent']
                    min_daterecv = subjectdict[subject]['min_daterecv']
                    max_datesent = subjectdict[subject]['max_datesent']
                    max_daterecv = subjectdict[subject]['max_daterecv']
                    importance = subjectdict[subject]['importance']
                    outfile.write(
                        "{},{},{},{},{},{},{},{}\n".format(index, count, subject, min_datesent, max_datesent,
                                                           min_daterecv, max_daterecv, importance))
                else:
                    error_count += 1
                    # print("{} not in file2".format(subject))
                index += 1

    print(error_count)


def handleTopicDate():
    file1 = "data/topic/weight&date/subject_1_date_sorted.txt"
    ldaFile = "data/output/ldaResult_topic-doc_w.txt"
    topicdict = dict()
    reversedTopicDict = dict()
    for i in range(20):
        topicdict[str(i)] = dict()  # { 0: { 0: {}, 1: {} } }
        # topicdict[str(i)]['subjects'] = dict()

    with open(ldaFile) as f:
        for line in f:
            array = line.strip().split(":")
            subject_idx = array[0]
            topic_idx = array[1]
            # topicdict[topic_idx]['subjects'][subject_idx] = dict()

            reversedTopicDict[subject_idx] = topic_idx

    with open(file1) as f:
        for line in f:
            array = line.strip().split(",")
            subject_idx = array[0]
            if subject_idx not in reversedTopicDict:
                continue
            count = int(array[1])
            subject = array[2].strip()
            min_datesent = helper.datetimeFromStr(1, array[3].strip(), None)
            max_datesent = helper.datetimeFromStr(1, array[4].strip(), None)
            min_daterecv = helper.datetimeFromStr(1, array[5].strip(), None)
            max_daterecv = helper.datetimeFromStr(1, array[6].strip(), None)
            importance = int(array[7])
            topic_idx = reversedTopicDict[subject_idx]
            # topicdict[topic_idx]['subjects'][subject_idx] = {
            #     'min_datesent': min_datesent,
            #     'min_daterecv': min_daterecv,
            #     'max_datesent': max_datesent,
            #     'max_daterecv': max_daterecv,
            #     'subject': subject,
            #     'count': count,
            #     'importance': importance
            # }
            year = min_datesent.year
            month = min_datesent.month
            if year not in topicdict[topic_idx]:
                topicdict[topic_idx][year] = dict()
                topicdict[topic_idx][year][month] = {'count': count, 'importance': importance}
            elif month not in topicdict[topic_idx][year]:
                topicdict[topic_idx][year][month] = {'count': count, 'importance': importance}
            else:
                topicdict[topic_idx][year][month]['count'] += count
                topicdict[topic_idx][year][month]['importance'] += importance

                # for i in range(20):
                # del topicdict[str(i)]['subjects']
                # array.append(topicdict[str(i)])
    # for topic_idx in topicdict:
    #     for year in topicdict[topic_idx]:
    #         for month in topicdict[topic_idx][year]:
    #             topicdict[topic_idx][year][month]['importance'] = topicdict[topic_idx][year][month]['importance'] / \
    #                                                               topicdict[topic_idx][year][month]['count']

    with open("data/output/topic_year_month_count.json", "w") as f:
        json.dump(topicdict, f, sort_keys=True)


def handleGant():
    file1 = "data/topic/weight&date/subject_1_date_sorted.txt"
    ldaFile = "data/output/ldaResult_topic-doc_w.txt"
    topicdict = list()
    reversedTopicDict = dict()
    for i in range(20):
        topicdict.append({'startDate': None, 'endDate': None, 'taskName': '', 'status': 0, 'count': 0})

    with open(ldaFile) as f:
        for line in f:
            array = line.strip().split(":")
            subject_idx = array[0]
            topic_idx = array[1]
            reversedTopicDict[subject_idx] = topic_idx

    with open(file1) as f:
        for line in f:
            array = line.strip().split(",")
            subject_idx = array[0]
            if subject_idx not in reversedTopicDict:
                continue
            count = int(array[1])
            subject = array[2].strip()
            min_datesent = helper.datetimeFromStr(1, array[3].strip(), None)
            max_datesent = helper.datetimeFromStr(1, array[4].strip(), None)
            # min_daterecv = helper.datetimeFromStr(1, array[5].strip(), None)
            # max_daterecv = helper.datetimeFromStr(1, array[6].strip(), None)
            importance = int(array[7])
            topic_idx = int(reversedTopicDict[subject_idx])

            topicdict[topic_idx]['taskName'] = 'topic' + str(topic_idx)
            topicdict[topic_idx]['count'] += count
            topicdict[topic_idx]['status'] += importance

            if topicdict[topic_idx]['startDate'] is None:
                topicdict[topic_idx]['startDate'] = min_datesent
            else:
                if topicdict[topic_idx]['startDate'] > min_datesent:
                    topicdict[topic_idx]['startDate'] = min_datesent
            if topicdict[topic_idx]['endDate'] is None:
                topicdict[topic_idx]['endDate'] = max_datesent
            else:
                if topicdict[topic_idx]['endDate'] < max_datesent:
                    topicdict[topic_idx]['endDate'] = max_datesent

    for item in topicdict:
        item['startDate'] = helper.dateTimeToStr(item['startDate'])
        item['endDate'] = helper.dateTimeToStr(item['endDate'])
        item['status'] = item['status'] / item['count'] * 5
    with open("data/output/gant.json", "w") as f:
        json.dump(topicdict, f, sort_keys=True)


def handleTopicDateJson():
    outarray = list()
    with open("data/topic/weight&date/topic_year_month_count.json") as f:
        topicdict = json.load(f)
        for i in range(20):
            topic_idx = str(i)
            topicItem = {}
            topicItem['name'] = 'topic' + topic_idx
            topicItem['region'] = 'topic' + topic_idx
            topicItem['count'] = []
            topicItem['importance'] = []
            outarray.append(topicItem)
            for year in topicdict[topic_idx]:
                sumcount = 0
                sumimportance = 0
                for month in topicdict[topic_idx][year]:
                    sumcount += topicdict[topic_idx][year][month]['count']
                    sumimportance += topicdict[topic_idx][year][month]['importance']
                topicItem['count'].append([int(year), sumcount])
                topicItem['importance'].append([int(year), sumimportance / sumcount * 5])
    with open("data/output/topic_year_2D.json", "w") as f:
        json.dump(outarray, f, sort_keys=True)


def handleDateTopicJson():
    outdict = dict()
    with open("data/topic/weight&date/topic_year_month_count.json") as f:
        topicdict = json.load(f)
        for i in range(20):
            topic_idx = str(i)
            for year in topicdict[topic_idx]:
                if year not in outdict:
                    outdict[year] = {"months": []}
                    for j in range(12):
                        topicArray = []
                        for k in range(20):
                            topicArray.append({'pc': 0})
                        outdict[year]['months'].append(topicArray)
                for month in topicdict[topic_idx][year]:
                    monthArray = outdict[year]['months']
                    topicArray = monthArray[int(month) - 1]
                    topicArray[i]['pc'] += topicdict[topic_idx][year][month]['count']

    with open("data/output/year_topic_2D.json", "w") as f:
        json.dump(outdict, f, sort_keys=True)


def handleDateTopicJson2():
    outdict = dict()
    outdict['all'] = {'years': []}
    for i in range(2001, 2016):
        outdict['all']['years'].append(list())

    with open("data/topic/weight&date/topic_year_month_count.json") as f:
        topicdict = json.load(f)
        for i in range(20):
            topic_idx = str(i)
            for j in range(2001, 2016):
                year = str(j)
                topicItem = {'pc': 0}
                if year in topicdict[topic_idx]:
                    for month in topicdict[topic_idx][year]:
                        topicItem['pc'] += topicdict[topic_idx][year][month]['count']

                outdict['all']['years'][j - 2001].append(topicItem)

    with open("data/output/year_topic_2D_2.json", "w") as f:
        json.dump(outdict, f, sort_keys=True)


def findTopNSubject():
    countArray = []
    countIdxDict = {}
    with open("data/topic/weight&date/subject_1_date_sorted.txt") as f:
        for line in f:
            array = line.strip().split(",")
            subject_idx = array[0]
            count = int(array[1])
            countArray.append(count)

            subject = array[2].strip()
            min_datesent = helper.datetimeFromStr(1, array[3].strip(), None)
            max_datesent = helper.datetimeFromStr(1, array[4].strip(), None)
            min_daterecv = helper.datetimeFromStr(1, array[5].strip(), None)
            max_daterecv = helper.datetimeFromStr(1, array[6].strip(), None)
            importance = int(array[7])

            if count not in countIdxDict:
                countIdxDict[count] = list()
                countIdxDict[count].append(subject)
            else:
                countIdxDict[count].append(subject)
    countArray.sort(reverse=True)

    with open("data/topic/weight&date/topNTopic.json", "w") as f:
        allSubjectList = list()
        outdict = {"label": allSubjectList, "count": []}
        for i in range(51):
            count = countArray[i]
            subjectList = countIdxDict[count]
            for subject in subjectList:
                allSubjectList.append(subject)
                # f.write("{},{}\n".format(count, subject))
        outdict['count'] = countArray[0: 51]
        json.dump(outdict, f)


def main():
    # subjectdict = handleOriginFile("data/topic/weight&date/subject1_w_date.txt")

    # termdict = handleSubject1("data/topic/subject2_w_date.txt")
    # genLdaInputDoc(None)
    # ldaTest()
    # nltkTest()
    # testRegex()
    # findSubjectByCategory()
    # resort("data/topic/weight/subject1_w.txt", "data/topic/weight&date/subject1_w_date.txt")
    # handleTopicDate()
    # handleTopicDateJson()
    # handleDateTopicJson2()
    # handleGant()
    findTopNSubject()

    print("over")


if __name__ == '__main__':
    main()
