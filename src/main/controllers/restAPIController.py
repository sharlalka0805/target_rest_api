from flask import request, jsonify
from src.main.utility.dbHelper import dbHelper
from src.main.utility.modelHelper import modelHelper
from src.main.enums.ResponseErrorMessage import ResponseErrorMessage
from flask import Blueprint

app01 = Blueprint('app01', __name__,template_folder='templates',static_folder='static')

modelHelper = modelHelper()
dbHelper = dbHelper()

################################  Route Functions - Start ###################################################

@app01.route('/')
def load_app():
    name = 'User'
    title = 'Welcome'
    return "<html><h1> This service is UP and Running ... !!! </h1></html>"

# Method to get list of available models , Add a model , Delete an existing model
@app01.route('/models', methods=['GET', 'PUT','DELETE'])
def getModelsList(modelName=None):
        print("inside getModelsList in restAPIController ")

        if request.method == 'PUT':
            print('Inside getModelsList: PUT')

            requestMessage = request.json
            message = modelHelper.addModel(requestMessage)

            if message == "Model added successfully":
                data = modelHelper.getModelList()

                if data is not None:
                    return data
                else:
                    return modelHelper.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)
        elif request.method == 'DELETE':
            modelName = request.args.get('model')
            print('Inside deleteModel = ', modelName)

            if modelName is not None:
                message = modelHelper.deleteModel(modelName)

                if message == "Model deleted successfully":
                    data = modelHelper.getModelList()

                    if data is not None:
                        return data
                    else:
                        return modelHelper.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)
                else:
                    return modelHelper.errorResponseMessage(ResponseErrorMessage.DATA_DOES_NOT_ALREADY_EXISTS.value)
            else:
                return modelHelper.errorResponseMessage(ResponseErrorMessage.MISSING_INFO.value)
        else:
            print('Inside getModelsList: GET')

            data = modelHelper.getModelList()
            if data is not None:
                return data
            else:
                return modelHelper.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)


# Answer a Question
@app01.route('/answer', methods=['POST'])
def findAnswer(modelName=None):
        modelName = request.args.get('model')

        if modelName == '':
            modelName = 'bert-base-multilingual-uncased'
            print('Inside  findAnswer using model =  ', modelName)

        # Fetch the request JSON
        requestMessage = request.json

        # Call the method to answer the questions
        answer = modelHelper.findAnswer(modelName, requestMessage)

        if answer is not None:
            return answer
        else:
            return modelHelper.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)

# List recently answered questions
@app01.route('/answer', methods=['GET'])
def listAnswers(modelName=None, startTime=None, endTime=None):

        # TODO:Check the optional and required conditions for the three parameters
        modelName = request.args.get('model')
        startTime = request.args.get('start')
        endTime = request.args.get('end')

        print('Inside restAPIHelper.listAnswers modelName = ',modelName,' startTime = ',startTime,' endTime = ',endTime)
        if startTime == '':
            return modelHelper.errorResponseMessage(ResponseErrorMessage.START_TIME.value)

        if endTime == '':
            return modelHelper.errorResponseMessage(ResponseErrorMessage.END_TIME.value)

        recentlyAnsweredQuestionsList = modelHelper.getRecentlyAnsweredQuestions(modelName, startTime, endTime)

        if recentlyAnsweredQuestionsList is not None:
            return recentlyAnsweredQuestionsList
        else:
            return modelHelper.errorResponseMessage(ResponseErrorMessage.ERORR_OCCUREED.value)

# Exception Handler
@app01.errorhandler(Exception)
def handle_exception(error):
        message = [str(x) for x in error.args]
        success = False
        response = {
            'success': success,
            'error': {
                'type': error.__class__.__name__,
                'message': message
            }
        }

        return jsonify(response)

################################  Route Functions - END ###################################################