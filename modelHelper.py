import json
from datetime import datetime

from dbHelper import dbHelper
from NLPModels import NLPModels
from questionAnswer import questionAnswer
from transformers.pipelines import pipeline
from ResponseErrorMessage import ResponseErrorMessage
from appLogger import appLogger
from actionTypes import actionTypes


# Method to find answer
class modelHelper:

    def __init__(self):
        self.db_helper = dbHelper()

    def findAnswer(self,modelName,requestMessage):
        print('Inside modelHelper.findAnswer for modelName = ',modelName)

        # Fetch the tokenizer details from DB for this model
        # If model not found in the current database - return error
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

            # Insert a log
            action_details = {'question':requestMessage['question']
                              ,'answer':answer
                              ,'context' : requestMessage['context']}

            #self.db_helper.saveDBLog(appLogger(modelName
             #              ,actionTypes.FIND_ANSWER.value
             #              ,action_details
             #              ,'USER'
              #             ,int(datetime.utcnow().timestamp())))

            # Return response json return json.dumps(question_answer, default=lambda x: x.__dict__)
            return action_details
        else:
            # Return response - In case model does not exist
            return self.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)

    # Method to fetch current list of models present in the system
    def getModelList(self):
        print('Inside modelHelper.getModelList')

        data = self.db_helper.listModels()
        print(data)

        if data is not None:

            # Define the list of class objects
            listOfModels = []
            for row in data:
                print(row[0], row[1], row[2])
                listOfModels.append({'name':row[0],'tokenizer':row[1],'model':row[2]})
            return listOfModels

    # Method to fetch the list of recently answered questions
    def getRecentlyAnsweredQuestions(self,modelName,startTime,endTime):
        print('Inside modelHelper.getRecentlyAnsweredQuestions')

        # Fetch the question_answer list
        data = self.db_helper.getRecentlyAnsweredQuestionsList(modelName,startTime,endTime)

        if len(data) > 1:
            listOfQuestionAnswer = []
            for row in data:
                print(row[0], row[1], row[2],row[3], row[4])
                listOfQuestionAnswer.append(questionAnswer(row[4], row[0], row[3],row[1], row[2]))

            #Add Log

            # Return response JSON json.dumps(listOfQuestionAnswer, default=lambda x: x.__dict__)
            return listOfQuestionAnswer
        else:
            # Return error JSON
            return self.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)

    # Method to add a new model
    def addModel(self,requestMessage):
        print('Inside modelHelper.addModel')

        # check if model already exists
        modelDetails = self.getModelDetails(requestMessage['name'])

        if modelDetails is not None:
            print('Inside modelHelper.addModel == Model alreday exists')
            return  self.errorResponseMessage(ResponseErrorMessage.DATA_ALREADY_EXISTS.value)
        else:
            print('Inside modelHelper.addModel == New Model')
            message = self.db_helper.addModel(requestMessage['name']
                                    , requestMessage['tokenizer']
                                    , requestMessage['model'])

            # Insert a log
            action_details = {'name': requestMessage['name']
                , 'tokenizer': requestMessage['tokenizer']
                , 'model': requestMessage['model']}

            #self.db_helper.saveDBLog(appLogger(requestMessage['name']
             #                                  , actionTypes.ADD_MODEL.value
              #                                 , action_details
             #                                  , 'USER'
              #                                 , int(datetime.utcnow().timestamp())))

            return message

    # Method to delete model details
    def deleteModel(self,modelName):
        print('Inside modelHelper.deleteModel for modelName = ',modelName)

        # check if model already exists
        modelDetails = self.getModelDetails(modelName)

        if modelDetails is None:
            print('Inside modelHelper.deleteModel == Model does not exists')
            return  self.errorResponseMessage(ResponseErrorMessage.DATA_DOES_NOT_ALREADY_EXISTS.value)
        else:
            print('Inside modelHelper.deleteModel == model to be deleted exists')
            message = self.db_helper.deleteModel(modelName)

            #Insert a log
            action_details = {'modelName': 'Delete the model'+ modelName}

            #self.db_helper.saveDBLog(appLogger(modelName
             #                                  , actionTypes.DELETE_MODEL.value
             #                                  , action_details
              #                                 , 'USER'
               #                                , int(datetime.utcnow().timestamp())))
            return message

    # Method to fetch details of a specific model
    def getModelDetails(self, modelName):
            print('Inside modelHelper.getModelDetails')

            # Fetch model details
            data = self.db_helper.getModelDetails(modelName)

            if data is not None:
                for row in data:
                    modelDetails = NLPModels(row[0], row[1], row[2])

                    # Return Model Details
                    return modelDetails
            else:
                pass


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

        #return json.dumps(response)
        return response

