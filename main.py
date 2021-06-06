import logging

from flask import Flask
from flask import request
from flask import jsonify
import time
from transformers import pipeline
import init as _init
import os
from gcloud import storage
import file_util

# Define Global Variables
models = {}
environment = ''
con = ''

logging.basicConfig(format='%(levelname)s:%(message)s')


# Create my flask app
def create_app():

    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "<p>The question answering API is healthy!</p>"

    # Define a handler for the /answer path, which
    # processes a JSON payload with a question and
    # context and returns an answer using a Hugging
    # Face model.
    @app.route("/answer", methods=['POST'])
    def answer():
        logging.info('Inside answer -- POST -->')

        try:
            # Get the request body data
            data = request.json

            # Validate model name if given
            if request.args.get('model') != None:
                if not validate_model(request.args.get('model')):
                    return "Model not found", 400

            # Answer the question
            answer, model_name = answer_question(request.args.get('model'),
                                                 data['question'], data['context'])
            timestamp = int(time.time())

            # Insert our answer in the database
            con = _init.init_db(environment)
            cur = con.cursor()
            sql = "INSERT INTO answers VALUES ('{question}','{context}','{model}','{answer}',{timestamp})"
            cur.execute(sql.format(
                question=data['question'].replace("'", "''"),
                context=data['context'].replace("'", "''"),
                model=model_name,
                answer=answer,
                timestamp=str(timestamp)))
            con.commit()
            con.close()

            # Create the response body.
            out = {
                "question": data['question'],
                "context": data['context'],
                "answer": answer,
                "model": model_name,
                "timestamp": timestamp
            }

            return jsonify(out)
        except Exception as ex:
            logging.error('Excecption occurred in answer' , ex)

    # List historical answers from the database.
    @app.route("/answer", methods=['GET'])
    def list_answer():
        logging.info('Inside answer -- GET -->')

        try:

            # Validate timestamps
            if request.args.get('start') == None or request.args.get('end') == None:
                return "Query timestamps not provided", 400

            # Prep SQL query
            if request.args.get('model') != None:
                sql = "SELECT * FROM answers WHERE timestamp >= {start} AND timestamp <= {end} AND model == '{model}'"
                sql_rev = sql.format(start=request.args.get('start'),
                                     end=request.args.get('end'), model=request.args.get('model'))
            else:
                sql = 'SELECT * FROM answers WHERE timestamp >= {start} AND timestamp <= {end}'
                sql_rev = sql.format(start=request.args.get('start'), end=request.args.get('end'))

            # Query the database
            con = _init.init_db(environment)
            cur = con.cursor()
            out = []
            for row in cur.execute(sql_rev):
                out.append({
                    "question": row[0],
                    "context": row[1],
                    "answer": row[2],
                    "model": row[3],
                    "timestamp": row[4]
                })
            con.close()

            return jsonify(out)
        except Exception as ex:
            logging.error('Exception occured in answer -- GET' , ex)

    # List models currently available for inference
    @app.route("/models", methods=['GET'])
    def list_model():
        logging.info('Inside get models --> ')
        try:
            # Get the loaded models
            models_loaded = []
            for m in models['models']:
                models_loaded.append({
                    'name': m['name'],
                    'tokenizer': m['tokenizer'],
                    'model': m['model']
                })
            return jsonify(models_loaded)
        except Exception as ex:
            logging.error('Exception occured in get models -- GET', ex)

    # Add a model to the models available for inference
    @app.route("/models", methods=['PUT'])
    def add_model():
        logging.info('Inside get models PUT --> ')

        try:
            # Get the request body data
            data = request.json

            if validate_model(data['name']):
                return "Model to be added already present", 400

            # Load the provided model
            if not validate_model(data['name']):
                models_rev = []
                for m in models['models']:
                    models_rev.append(m)
                models_rev.append({
                    'name': data['name'],
                    'tokenizer': data['tokenizer'],
                    'model': data['model'],
                    'pipeline': pipeline('question-answering',
                                         model=data['model'],
                                         tokenizer=data['tokenizer'])
                })
                models['models'] = models_rev

            # Get the loaded models
            models_loaded = []
            for m in models['models']:
                models_loaded.append({
                    'name': m['name'],
                    'tokenizer': m['tokenizer'],
                    'model': m['model']
                })

            return jsonify(models_loaded)
        except Exception as ex:
            logging.error('Exception occured in get models -- PUT', ex)

    # Delete a model from the models available for inference
    @app.route("/models", methods=['DELETE'])
    def delete_model():
        logging.info('delete_model --> DELETE')
        try:

            # Validate model name if given
            if request.args.get('model') == None:
                return "Model name not provided in query string", 400

            # Error if trying to delete default model
            if request.args.get('model') == models['default']:
                return "Can't delete default model", 400

            if not validate_model(request.args.get('model')):
                return "Model to be deleted not present", 400

            # Load the provided model
            models_rev = []
            for m in models['models']:
                if m['name'] != request.args.get('model'):
                    models_rev.append(m)
            models['models'] = models_rev

            # Get the loaded models
            models_loaded = []
            for m in models['models']:
                models_loaded.append({
                    'name': m['name'],
                    'tokenizer': m['tokenizer'],
                    'model': m['model']
                })

            return jsonify(models_loaded)
        except Exception as ex:
            logging.error('Exception occured in get models -- DELETE', ex)

    # Method to accept a csv and save it in a cloud storage
    @app.route("/upload", methods=['POST'])
    def uploadCSV():
        logging.info('Inside upload CSV --> POST')
        try:
            input_csv = request.files['file']
            logging.info('Inside uploadCSV --> File fetched ')
            if input_csv is not None:
                file_util.init(environment)
                file_util.uploadOneFile('question-answer','question',input_csv)
        except Exception as ex:
            logging.error('Exception occured in upload CSV', ex)


    # ---------------------------------#
    #  FUNCTIONS   #
    # ----------------------------------#

    # Validate that a model is available
    def validate_model(model_name):
        # Get the loaded models
        model_names = []
        for m in models['models']:
            model_names.append(m['name'])

        return model_name in model_names

    # Answer a question with a given model name
    def answer_question(model_name, question, context):
        # Get the right model pipeline
        if model_name == None:
            for m in models['models']:
                if m['name'] == models['default']:
                    model_name = m['name']
                    hg_comp = m['pipeline']
        else:
            for m in models['models']:
                if m['name'] == model_name:
                    hg_comp = m['pipeline']

        # Answer the answer
        answer = hg_comp({'question': question, 'context': context})['answer']

        return answer, model_name

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


# Run main by default if running "python answer.py"
if __name__ == '__main__':

    environment = 'LOCAL'
    models = _init.getInitialModel()

    app = create_app()

    # Run our Flask app and start listening for requests!
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), threaded=True,debug=True)