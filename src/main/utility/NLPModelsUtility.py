import json
from src.main.utility.dbHelper import dbHelper
from src.main.models.NLPModels import NLPModels

class NLPModelsUtility:

#TODO : create init method and move object instatiation
    def findAnswer(modelName):
        # Read the input data
        # run the required model
        # fetch the answer
        # do exceptionhandling
        # create the json and sne back
        # do logging
        return "thank you for choosing us"

    def getModelList(self):
        dbHelperObj = dbHelper()
        data = dbHelperObj.listModels()
        if data is not None:
            # Define the list of classs objects
            listOfModels = []
            for row in data:
                print(row[0], row[1], row[2])
                listOfModels.append(NLPModels(row[0], row[1], row[2]))
            return json.dumps(listOfModels, default=lambda x: x.__dict__)

    def getRecentlyAnsweredQuestions(self,modelName,startTime,endTime):

        return "question-anser list "

    def errorResponseMessage(self, message):
        return json.dumps(message)



