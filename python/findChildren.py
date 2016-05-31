import codecs
import csv

from LineData import *


def main():
    outfile = "data/json/children.json"
    dataDir = "data/After2/"
    filename = "d.martinez_2.csv"
    f = csv.reader(codecs.open(dataDir + filename, "r", "iso-8859-1"))
    header = f.__next__()

    originDataDict = dict()

    for line in f:
        if len(line) > 1:
            data = LineData(line)
            if data.getCcDis() != "":
                originDataDict[(data.getCcDis(), data.getFromDis())] = 1

    print(len(originDataDict))



if __name__ == '__main__':
    main()
