from flask import Flask
from src.main.controllers import restAPIController
from src.main.utility.dbHelper import dbHelper
from src.main.utility.modelHelper import modelHelper


# Initialize the app
app = Flask(__name__)
app.register_blueprint(restAPIController.app01)

if __name__ == '__main__':

    db_helper = dbHelper()
    message = db_helper.initialSetUp()
    print(message)

    modelHelper = modelHelper()

    # Run our Flask app
    app.run(host='0.0.0.0', port=5000, threaded=True,debug=True)

