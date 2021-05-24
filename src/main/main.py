import json
from flask import Flask
from werkzeug.exceptions import HTTPException
from flask import request, jsonify
from src.main.utility.dbHelper import dbHelper
from src.main.utility.NLPModelsUtility import NLPModelsUtility
from src.main.enums.ResponseErrorMessage import ResponseErrorMessage

# Initialize the app
app = Flask(__name__)

dbHelperObject = dbHelper()
NLPModelsUtilityObj = NLPModelsUtility()

################################  Route Functions - Start ###################################################

@app.route('/')
def load_app():
    name = 'User'
    title = 'Welcome'
    return "<html><h1> This service is UP and Running ... !!! </h1></html>"


@app.route('/models', methods=['GET','POST'])
def getModelsList():
    print("inside getModelsList in main ")

    if request.method == 'POST':
        print('Inside getModelsList: POST')

        requestMessage = request.json
        message = dbHelperObject.addModel(requestMessage['name'], requestMessage['tokenizer'], requestMessage['model'])

        if message == "Model added successfully":
            data = NLPModelsUtilityObj.getModelList()

            if data is not None:
                return jsonify(data)
            else:
                return NLPModelsUtilityObj.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND)
    else:
        print('Inside getModelsList: GET')
        data = NLPModelsUtilityObj.getModelList()
        if data is not None:
            return jsonify(data)
        else:
            return NLPModelsUtilityObj.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND)

# Delete a Model
@app.route('/models/<modelName>', methods=['DELETE'])
def deleteModel(modelName):
    print('Inside deleteModel = ' , modelName)

    # TODO: add validation for model Name

    if modelName is not None:
        message = dbHelperObject.deleteModel(modelName)

        if message == "Model deleted successfully":
            data = NLPModelsUtilityObj.getModelList()

            if data is not None:
                return jsonify(data)
            else:
                return NLPModelsUtilityObj.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND)
    else:
        return NLPModelsUtilityObj.errorResponseMessage(ResponseErrorMessage.MISSING_INFO)


# Answer a Question
@app.route('/answer/<modelName>', methods=['POST'])
def findAnswer(modelName):
    print('Inside findAnswer using model =  ', modelName)

    # TODO: IF user has not provided any model name,pick this default model
    if modelName is None:
        modelName = ''

    # Fetch the request JSON
    requestMessage = request.json

    # Call the method to answer the questions
    answer = NLPModelsUtilityObj.findAnswer(modelName, requestMessage)

    if answer is not None:
        return jsonify(answer)
    else:
        return NLPModelsUtilityObj.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND)


# List recently answered questions
@app.route('/answer/<modelName>/<startTime>/<endTime>', methods=['GET'])
def listAnswers(modelName,startTime,endTime):

    #TODO:Check the optional and required conditions for the three parameters

    if startTime is None:
        return NLPModelsUtilityObj.errorResponseMessage(ResponseErrorMessage.START_TIME)

    if endTime is None:
        return NLPModelsUtilityObj.errorResponseMessage(ResponseErrorMessage.END_TIME)

    recentlyAnsweredQuestionsList = NLPModelsUtilityObj.getRecentlyAnsweredQuestions(modelName,startTime,endTime)

    if recentlyAnsweredQuestionsList is not None:
        return jsonify(recentlyAnsweredQuestionsList)
    else:
        return NLPModelsUtilityObj.errorResponseMessage(ResponseErrorMessage.ERORR_OCCUREED)

@app.errorhandler(Exception)
def handle_exception(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    return jsonify(response), status_code


################################  Route Functions - END ###################################################

if __name__ == '__main__':

    # call for database set up
    message = dbHelperObject.initialSetUp()
    print(message)

    # Run our Flask app
    app.run(host='0.0.0.0', port=5000, threaded=True,debug=True)

