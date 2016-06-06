import codecs
import csv
import json

from LineData import *


def addNode(name, nodes, count):
    """
    :param name: str
    :param nodes: dict
    :param count: int
    :return: int
    """
    if name not in nodes:
        nodes[name] = count
        count += 1
    return count


def addLink(data, links, nodes):
    """
    :type data: LineData
    :type links: dict
    :type nodes: dict
    :return:
    """
    fromDis = data.getFromDis()
    toDis = data.getToDis()
    if fromDis in nodes and toDis in nodes:
        key = (fromDis, toDis)
        if key in links:
            links[key] += 1
        else:
            links[key] = 1


def main():
    outfile = "data/out/source_target.json"
    dataDir = "data/After2/"
    filename = "d.martinez_2.csv"
    f = csv.reader(codecs.open(dataDir + filename, "r", "iso-8859-1"))
    header = f.__next__()

    nodes = dict()
    links = dict()
    count = 0

    for line in f:
        if len(line) > 1:
            data = LineData(line)
            count = addNode(data.getFromDis(), nodes, count)
            count = addNode(data.getToDis(), nodes, count)
            addLink(data, links, nodes)

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
