class Results:
    numOfResults = 0
    plagiarismList=[]
    documentList = []
    matchingLines={}
    globalSimilarity=0
    matchingBlocks={}
    componentDocuments=[]
    def __init__(self, numOfResults=0, documentList=[],plagiarismList=[],matchingLines=None,globalSimilarity=None,matchingBlocks=None,componentDocuments=[]):
        self.numOfResults = numOfResults
        self.documentList = documentList
        self.matchingLines=matchingLines
        self.globalSimilarity=globalSimilarity
        self.matchingBlocks=matchingBlocks
        self.plagiarismList=plagiarismList
        self.componentDocuments=componentDocuments

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

    def setGlobalSimilarity(self,globalSimilarity):
        self.globalSimilarity=globalSimilarity

    def getGlobalSimilarity(self):
        return self.globalSimilarity

    def setMatchingBlocks(self, matchingBlocks):
        self.matchingBlocks=matchingBlocks

    def getMatchingBlocks(self):
        return self.matchingBlocks

    def setPlagiarismList(self,plagiarismList):
        self.plagiarismList=plagiarismList

    def getPlagiarismList(self):
        return  self.plagiarismList

    def setComponentDocuments(self,componentDocuments):
        self.componentDocuments=componentDocuments

    def getComponentDocuments(self):
        return self.componentDocuments

    def toString(self):
        print("number of results")
        print(self.numOfResults)
        print("global similarity:")
        print(self.globalSimilarity)
        print("combined matching blocks")
        print(self.matchingBlocks)
        print("component documents")
        print(self.componentDocuments)
        # print("maching lines")
        # print(self.matchingLines)
        print("plagiarism list")
        print(self.plagiarismList)
        print("relevant documents")
        print(self.documentList)