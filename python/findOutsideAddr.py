import helper
import csv
import codecs
import os
import LineData


def handleFile(input, nameSet, nameDict):
    f = csv.reader(codecs.open(input, "r", "iso-8859-1"))
    header = f.__next__()

    for line in f:
        if len(line) > 1:
            # data = LineData.LineData(line)
            # if not helper.isInternal(data.getFromDis(), data.getFromAddr(), nameDict):
            #     nameSet.add(data.getFromDis().strip())
            #
            # if not helper.isInternal(data.getToDis(), data.getToAddr(), nameDict):
            #     nameSet.add(data.getToDis().strip())
            #
            # if not helper.isInternal(data.getCcDis(), data.getCcAddr(), nameDict):
            #     nameSet.add(data.getCcDis().strip())
            #
            # if not helper.isInternal(data.getBccDis(), data.getBccAddr(), nameDict):
            #     nameSet.add(data.getBccDis().strip())

            originFrom = str(line[0]).strip().lower()
            originTo = str(line[1]).strip().lower()

            if originFrom not in nameDict:
                if "@hackingteam.it" not in originFrom:
                    nameSet.add(originFrom)

            if originTo not in nameDict:
                if "@hackingteam.it" not in originTo:
                    nameSet.add(originTo)


def main():
    nameDict = helper.loadEmployeeSet()
    dataDir = "data/After4"
    print(dataDir)

    toOut = "data/outsideName.txt"

    nameSet = set()

    fileList = os.listdir(dataDir)
    for filename in fileList:
        print(filename)
        handleFile(dataDir + "/" + filename, nameSet, nameDict)

    print(len(nameSet))

    count = 0
    f = open(toOut, "w")
    for name in nameSet:
        f.write(name + "\n")
        count += 1
        if count % 500 == 0:
            f.flush()
    f.close()


if __name__ == '__main__':
    main()
