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
    :type data: str
    :type links: dict
    :type nodes: dict
    :return:
    """
    fromDis = data[0]
    toDis = data[1]
    if fromDis in nodes and toDis in nodes:
        key = (fromDis, toDis)
        if key in links:
            print("repeat")
        else:
            links[key] = data[5]


def main():
    outfile = "data/json/source_target.json"
    dataDir = "data/After4/"
    filename = "all_4_to.csv"
    f = csv.reader(codecs.open(dataDir + filename, "r", "iso-8859-1"))
    header = f.__next__()

    nodes = dict()
    links = dict()
    id = 0

    for line in f:
        if len(line) > 1:
            id = addNode(line[0], nodes, id)
            id = addNode(line[1], nodes, id)
            addLink(line, links, nodes)

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
    main()
