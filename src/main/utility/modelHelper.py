import json
from datetime import datetime, time

from src.main.utility.dbHelper import dbHelper
from src.main.models.NLPModels import NLPModels
from src.main.models.questionAnswer import questionAnswer
from transformers.pipelines import pipeline
from src.main.enums.ResponseErrorMessage import ResponseErrorMessage


class modelHelper:

    def __init__(self):
        self.db_helper = dbHelper()

#TODO : create init method and move object instatiation

    def findAnswer(self,modelName,requestMessage):
        print('Inside modelHelper.findAnswer for modelName = ',modelName)

        # Fetch the tokenizer details from DB for this model - If model not found in the current database - return error
        modelDetails = self.getModelDetails(modelName)
        print('Inside modelHelper.findAnswer for modelDetails = ',modelDetails)

        if modelDetails is not None:

            # Import the required model
            hg_comp = pipeline('question-answering', model=modelDetails.model, tokenizer=modelDetails.tokenizer)

            # Answer the question
            answer = hg_comp({'question': requestMessage['question'], 'context': requestMessage['context']})['answer']

            print('Answer found = ' , answer)
            # Create question answer data object
            question_answer = questionAnswer(int(datetime.utcnow().timestamp())
                                            ,modelDetails.model
                                             ,answer
                                             ,requestMessage['question']
                                             ,requestMessage['context'])

            # save data in table
            self.db_helper.saveRecentlyAnsweredQuestion(question_answer)

            # TODO: log an entry in logger

            # return responcse json
            return json.dumps(question_answer, default=lambda x: x.__dict__)
        else:
            self.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)



    def getModelList(self):
        print('Inside modelHelper.getModelLis')

        data = self.db_helper.listModels()

        if data is not None:
            # Define the list of class objects
            listOfModels = []
            for row in data:
                print(row[0], row[1], row[2])
                #listOfModels.append(NLPModels(row[0], row[1], row[2]))
                listOfModels.append({'name':row[0],'tokenizer':row[1],'model':row[2]})
            return json.dumps(listOfModels)

    def getRecentlyAnsweredQuestions(self,modelName,startTime,endTime):
        print('Inside modelHelper.getRecentlyAnsweredQuestions')

        data = self.db_helper.getRecentlyAnsweredQuestionsList(modelName,startTime,endTime)
        print(data)

        if len(data) > 1:
            listOfQuestionAnswer = []
            for row in data:
                print(row[0], row[1], row[2],row[3], row[4])
                listOfQuestionAnswer.append(questionAnswer(row[4], row[0], row[3],row[1], row[2]))
            return json.dumps(listOfQuestionAnswer, default=lambda x: x.__dict__)
        else:
            return self.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)

    def errorResponseMessage(self, message):
        print('Inside errorResponseMessage message = ',message)
        success = False
        response = {
            'success': success,
            'error': {
                'type': '600',
                'message': message
            }
        }

        return json.dumps(response)

    def getModelDetails(self,modelName):
        print('Inside modelHelper.getModelDetails')

        data = self.db_helper.getModelDetails(modelName)

        if data is not None:
            for row in data:
                modelDetails = NLPModels(row[0],row[1],row[2])
                return modelDetails
        else:
            pass

    def addModel(self,requestMessage):
        print('Inside modelHelper.addModel')

        #check if model already exists
        modelDetails = self.getModelDetails(requestMessage['name'])

        if modelDetails is not None:
            print('Inside modelHelper.addModel == Model alreday exists')
            return  self.errorResponseMessage(ResponseErrorMessage.DATA_ALREDAY_EXISTS.value)
        else:
            print('Inside modelHelper.addModel == New Model')
            message = self.db_helper.addModel(requestMessage['name']
                                    , requestMessage['tokenizer']
                                    , requestMessage['model'])
            # TODO: log an entry in logger

            return message


    def deleteModel(self,modelName):
        print('Inside modelHelper.deleteModel for modelName = ',modelName)

        # check if model already exists
        modelDetails = self.getModelDetails(modelName)

        if modelDetails is None:
            print('Inside modelHelper.deleteModel == Model does not exists')
            return  ResponseErrorMessage.DATA_ALREDAY_EXISTS
        else:
            print('Inside modelHelper.deleteModel == model to be delted exists')
            message = self.db_helper.deleteModel(modelName)
            # TODO: log an entry in logger
            return message



