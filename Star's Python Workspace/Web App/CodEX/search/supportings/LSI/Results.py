class Results:
    numOfResults = 0
    documents = [] #[(docName,[maching line numbers])]

    def __init__(self, numOfResults=0, documents=[]):
        self.numOfResults = numOfResults
        self.documents = documents

    def getNumOfResults(self):
        return self.numOfResults

    def setNumOfResult(self, num):
        self.numOfResults = num

    def getDocuments(self):
        return self.documents

    def setDocuments(self, documents):
        self.documents = documents

