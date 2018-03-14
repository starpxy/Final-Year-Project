class Results:
    numOfResults = 0
    documentList = []

    def __init__(self, numOfResults=0, documentList=[]):
        self.numOfResults = numOfResults
        self.documentList = documentList

    def getNumOfResults(self):
        return self.numOfResults

    def setNumOfResult(self, num):
        self.numOfResults = num

    def getDocumentList(self):
        return self.documentList

    def setDocumentList(self, documentList):
        self.documentList = documentList
