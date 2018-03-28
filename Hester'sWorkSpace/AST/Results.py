class Results:
    numOfResults = 0
    documentList = []
    matchingLines={}

    def __init__(self, numOfResults=0, documentList=[],matchingLines=None):
        self.numOfResults = numOfResults
        self.documentList = documentList
        self.matchingLines=matchingLines

    def getNumOfResults(self):
        return self.numOfResults

    def setNumOfResult(self, num):
        self.numOfResults = num

    def getDocumentList(self):
        return self.documentList

    def setDocumentList(self, documentList):
        self.documentList = documentList

    def setMatchingLines(self,matchingLines):
        self.matchingLines=matchingLines

    def getMatchingLines(self):
        return self.matchingLines
