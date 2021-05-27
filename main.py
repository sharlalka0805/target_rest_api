from flask import Flask
from dbHelper import dbHelper
from modelHelper import modelHelper


# Initialize the app
app = Flask(__name__)
app.register_blueprint(restAPIController.app01)

if __name__ == '__main__':

    db_helper = dbHelper()

    # Do the initial DB setup
    db_helper.createDatabase()
    message = db_helper.insertInitialData()
    print(message)

    modelHelper = modelHelper()

    # Run our Flask app
    app.run(host='0.0.0.0', port=8080, threaded=True,debug=True)

