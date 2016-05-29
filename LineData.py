class LineData(object):
    def __init__(self, data):
        self.line = data

    def getSubject(self):
        return self.line[0]

    def getFromDis(self):
        return self.line[1]

    def getFromAddr(self):
        return self.line[2]

    def getToDis(self):
        return self.line[3]

    def getToAddr(self):
        return self.line[4]

    def getCcDis(self):
        return self.line[5]

    def getCcAddr(self):
        return self.line[6]
