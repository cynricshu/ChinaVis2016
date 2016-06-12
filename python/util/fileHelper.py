import csv
import codecs
import sys

csv.field_size_limit(2 ** 31)
_flush_count = 1000


def readCsv(filename, func, *container):
    f = csv.reader(codecs.open(filename, "r", "iso-8859-1"))
    header = f.__next__()

    lineNum = 1
    for line in f:
        func(line, lineNum, container)
        lineNum += 1


def writeIterableToFile(filename, dataCollection):
    count = 0
    f = open(filename, "w")
    for data in dataCollection:
        f.write(data + "\n")
        count += 1
        if count % _flush_count == 0:
            f.flush()
    f.close()


def writeIterableToFileWithIndex(filename, dataCollection):
    f = open(filename, "w")
    for i in range(len(dataCollection)):
        f.write(dataCollection[i] + "\n")
        if i % _flush_count == 0:
            f.flush()
    f.close()


def writeDictToFile(filename, dataDict, genOutputStr):
    count = 0
    f = open(filename, "w")
    for key in dataDict:
        # f.write("{}:{}:{}:{}\n".format(dataDict[data][0], dataDict[data][1], dataDict[data][2], data))
        f.write(genOutputStr(key, dataDict[key]))
        count += 1
        if count % _flush_count == 0:
            f.flush()
    f.close()
