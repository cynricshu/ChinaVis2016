import csv
import codecs
import sys

csv.field_size_limit(sys.maxsize)
_flush_count = 1000


def readCsv(filename, func, *container):
    f = csv.reader(codecs.open(filename, "r", "iso-8859-1"))
    header = f.__next__()

    for line in f:
        if len(line) > 1:
            func(line, container)


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
        if i % 500 == 0:
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
