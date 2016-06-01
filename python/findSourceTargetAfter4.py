import codecs
import csv
import json
import xml
import xml.dom.minidom as minidom
from LineData import *


def loadEmployeeSet():
    """
    :return: dict
    """
    nameDict = dict()
    f = codecs.open("data/before_file_names.txt", "r", "iso-8859-1")
    for line in f:
        data = str(line)[0:-2].split(",")
        if len(data) == 1:
            nameDict[data[0].lower()] = data[0].lower()
            nameDict[data[0].lower() + "@hackingteam.it"] = data[0].lower()
        else:
            nameDict[data[0].lower()] = data[0].lower()
            nameDict[data[0].lower() + "@hackingteam.it"] = data[0].lower()
            nameDict[data[1].lower()] = data[0].lower()
            nameDict[data[1].lower() + "@hackingteam.it"] = data[0].lower()

    print(len(nameDict))
    # for item in nameSet:
    #     print(item)
    f.close()
    return nameDict


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


def addLink(fromDis, toDis, nodes, links, weight):
    """
    :type data: str
    :type links: dict
    :type nodes: dict
    :return:
    """
    if fromDis in nodes and toDis in nodes:
        key = (nodes[fromDis], nodes[toDis])
        if key in links:
            # print("repeat: %s" % str(key))
            value = links[key]
            value += int(weight)
            links[key] = value
        else:
            links[key] = int(weight)


def dumpJson(nodes, links, outfile):
    """
    :param nodes: dict
    :param links: dict
    :return:
    """
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
    out.flush()
    out.close()


def dumpXML(nodes, links, outfile):
    nodes2 = dict()
    for key in nodes:
        nodes2[nodes[key]] = key

    doc = minidom.Document()
    gexf = doc.createElement('gexf')
    gexf.setAttribute("xmlns:viz", "http:///www.gexf.net/1.1draft/viz")
    gexf.setAttribute("version", "1.1")
    gexf.setAttribute("xmlns", "http://www.gexf.net/1.1draft")
    doc.appendChild(gexf)

    meta = doc.createElement("meta")
    creator_text = doc.createTextNode("Gephi 0.7")
    creator = doc.createElement("creator")
    creator.appendChild(creator_text)
    meta.appendChild(creator)
    gexf.appendChild(meta)

    graph = doc.createElement("graph")
    graph.setAttribute("defaultedgetype", "directed")
    graph.setAttribute("idtype", "string")
    graph.setAttribute("type", "static")
    gexf.appendChild(graph)

    nodes = doc.createElement("nodes")
    graph.appendChild(nodes)

    count = 0
    for i in range(len(nodes2)):
        node = doc.createElement("node")
        node.setAttribute("id", str(float(i)))
        node.setAttribute("label", nodes2[i])
        nodes.appendChild(node)
        count += 1
        # if count >= 500:
        #     break

    nodes.setAttribute("count", str(len(nodes2)))
    # nodes.setAttribute("count", str(count))

    edges = doc.createElement("edges")
    graph.appendChild(edges)

    index = 0
    for key in links:
        edge = doc.createElement("edge")
        edge.setAttribute("id", str(index))
        edge.setAttribute("source", str(float(key[0])))
        edge.setAttribute("target", str(float(key[1])))
        edge.setAttribute("weight", str(float(links[key])))
        edges.appendChild(edge)
        index += 1
        # if index >= 1000:
        #     break

    edges.setAttribute("count", str(len(links)))
    # edges.setAttribute("count", str(index))

    f = open(outfile, "w")
    f.write(doc.toprettyxml(indent='    '))
    f.flush()
    f.close()


def handleFile(dataDir, input, output, nameDict):
    f = csv.reader(codecs.open(dataDir + input, "r", "iso-8859-1"))
    header = f.__next__()

    nodes = dict()
    links = dict()
    id = 0

    for line in f:
        if len(line) > 1:
            originFrom = str(line[0]).strip().lower()
            originTo = str(line[1]).strip().lower()
            if originFrom in nameDict and originTo in nameDict:
                id = addNode(nameDict[originFrom], nodes, id)
                id = addNode(nameDict[originTo], nodes, id)
                addLink(nameDict[originFrom], nameDict[originTo], nodes, links, line[5])

    dumpXML(nodes, links, output + ".gexf")
    dumpJson(nodes, links, output + ".json")


def main():
    dataDir = "data/After4/"

    toOut = "data/json/source_target_to"
    ccOut = "data/json/source_target_cc"
    bccOut = "data/json/source_target_bcc"
    output = [toOut, ccOut, bccOut]

    filename = "all_4_to.csv"
    ccFilename = "all_4_cc.csv"
    bccFilename = "all_4_bcc.csv"
    input = [filename, ccFilename, bccFilename]

    nameDict = loadEmployeeSet()

    index = 0
    for i in range(len(input)):
        handleFile(dataDir, input[i], output[i], nameDict)


if __name__ == '__main__':
    main()
