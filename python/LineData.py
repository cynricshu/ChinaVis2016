class LineData(object):
    def __init__(self, data):
        self.line = data

    def getSubject(self):
        """
        :rtype: str
        """
        return self.line[0]

    def getFromDis(self):
        """
        :rtype: str
        """
        return self.line[1]

    def getFromAddr(self):
        """
        :rtype: str
        """
        return self.line[2]

    def getToDis(self):
        """
        :rtype: str
        """
        return self.line[3]

    def getToAddr(self):
        """
        :rtype: str
        """
        return self.line[4]

    def getCcDis(self):
        """
        :rtype: str
        """
        return self.line[5]

    def getCcAddr(self):
        """
        :rtype: str
        """
        return self.line[6]

    def getBccDis(self):
        """
        :rtype: str
        """
        return self.line[7]

    def getBccAddr(self):
        """
        :rtype: str
        """
        return self.line[8]

    def getImportance(self):
        """
        :rtype: int
        """
        return int(self.line[10])

    def getDateSent(self):
        """
        :rtype: str
        """
        return self.line[11]

    def getDateReceive(self):
        """
        :rtype: str
        """
        return self.line[12]
