import codecs
import csv
import json

from LineData import *


def main():
    outfile = "data/json/import.json"
    dataDir = "data/After4/"
    filename = "all_4_to.csv"
    f = csv.reader(codecs.open(dataDir + filename, "r", "iso-8859-1"))
    header = f.__next__()

    nodes = dict()
    links = dict()
    count = 0

    for line in f:
        if len(line) > 1:
            data = LineData(line)

    nodeArray = []
    nodes2 = dict()
    for key in nodes:
        nodes2[nodes[key]] = key

    for i in range(len(nodes2)):
        nodeArray.append({"name": nodes2[i], "group": 1})

    linkArray = []
    for key in links:
        linkArray.append({"source": key[0], "target": key[1], "value": links[key]})

    final = {"nodes": nodeArray, "links": linkArray}

    out = open(outfile, "w")
    json.dump(final, out)
    # out.write(linksJson)
    out.flush()
    out.close()


if __name__ == '__main__':
    # commandline execution

    # args = sys.argv[1:]
    # if (len(args) < 5):
    #     print('error: arguments: user \"password\" db table csvfile')
    #     sys.exit(1)

    main()
