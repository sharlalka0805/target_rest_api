from flask import Flask
from flask import request, jsonify
from ResponseErrorMessage import ResponseErrorMessage
from dbHelper import dbHelper
from modelHelper import modelHelper


################################  Route Functions - Start ###################################################
def create_app():

    # Initialize the app
    app = Flask(__name__,instance_relative_config=True)

    @app.route('/')
    def load_app():
        name = 'User'
        title = 'Welcome'
        return "<html><h1> This service is UP and Running ... !!! </h1></html>"

    # Method to get list of available models , Add a model , Delete an existing model
    @app.route('/models', methods=['GET', 'PUT','DELETE'])
    def getModelsList(modelName=None):
            print("inside getModelsList in restAPIController ")

            if request.method == 'PUT':
                print('Inside getModelsList: PUT')

                requestMessage = request.json
                message = modelHelper.addModel(requestMessage)

                if message == "Model added successfully":
                    data = modelHelper.getModelList()

                    if data is not None:
                        return jsonify(data)
                    else:
                        return modelHelper.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)
                else:
                    return message
            elif request.method == 'DELETE':
                modelName = request.args.get('model')
                print('Inside deleteModel = ', modelName)

                if modelName is not None:
                    message = modelHelper.deleteModel(modelName)

                    if message == "Model deleted successfully":
                        data = modelHelper.getModelList()

                        if data is not None:
                            return jsonify(data)
                        else:
                            return modelHelper.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)
                    else:
                        return message
                else:
                    return modelHelper.errorResponseMessage(ResponseErrorMessage.MISSING_INFO.value)
            else:
                print('Inside getModelsList: GET')

                data = modelHelper.getModelList()
                if data is not None:
                    return jsonify(data)
                else:
                    return modelHelper.errorResponseMessage(ResponseErrorMessage.DATA_NOT_FOUND.value)


    # Answer a Question
    @app.route('/answer', methods=['POST'])
    def findAnswer(modelName=None):
            modelName = request.args.get('model')

            if modelName == '':
                modelName = 'bert-base-multilingual-uncased'
                print('Inside  findAnswer using model =  ', modelName)

            # Fetch the request JSON
            requestMessage = request.json

            if requestMessage is None:
                return modelHelper.errorResponseMessage(ResponseErrorMessage.Question_Not_Asked.value)

            # Call the method to answer the questions
            answer = modelHelper.findAnswer(modelName, requestMessage)

            return jsonify(answer)

    # List recently answered questions
    @app.route('/answer', methods=['GET'])
    def listAnswers(modelName=None, startTime=None, endTime=None):

            modelName = request.args.get('model')

            if modelName == '':
                modelName = 'bert-base-multilingual-uncased'
                print('Inside  findAnswer using model =  ', modelName)

            startTime = request.args.get('start')
            endTime = request.args.get('end')

            print('Inside restAPIHelper.listAnswers modelName = ',modelName,' startTime = ',startTime,' endTime = ',endTime)
            if startTime == '':
                return modelHelper.errorResponseMessage(ResponseErrorMessage.START_TIME.value)

            if endTime == '':
                return modelHelper.errorResponseMessage(ResponseErrorMessage.END_TIME.value)

            recentlyAnsweredQuestionsList = modelHelper.getRecentlyAnsweredQuestions(modelName, startTime, endTime)

            if recentlyAnsweredQuestionsList is not None:
                return jsonify(recentlyAnsweredQuestionsList)
            else:
                return modelHelper.errorResponseMessage(ResponseErrorMessage.ERORR_OCCUREED.value)


    # Exception Handler
    @app.errorhandler(Exception)
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
    return app

################################  Route Functions - END ###################################################

if __name__ == '__main__':

    modelHelper = modelHelper()
    dbHelper = dbHelper()

    # Do the initial DB setup
    message = dbHelper.createDatabase()
    print(message)

    # Create the app
    app = create_app()

    # Run our Flask app
    app.run(host='0.0.0.0', port=8080, threaded=True,debug=True)

