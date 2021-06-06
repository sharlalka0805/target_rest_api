from transformers import pipeline
import os
import stat
import psycopg2
import sqlite3 as sql


def getDBString_PROD():

    # Format DB connection information
    sslmode = "sslmode=verify-ca"

    # Format DB connection information
    sslrootcert_var = os.environ.get('PG_SSLROOTCERT')
    sslrootcert_var = sslrootcert_var.replace('@', '=')
    file = open("/server-ca.pem", "w")
    file.write(sslrootcert_var)
    file.close()
    os.chmod("/server-ca.pem", stat.S_IRUSR)
    os.chmod("/server-ca.pem", stat.S_IWUSR)
    sslrootcert = "sslrootcert=/server-ca.pem"

    sslcert_var = os.environ.get('PG_SSLCERT')
    sslcert_var = sslcert_var.replace('@', '=')
    file = open("/client-cert.pem", "w")
    file.write(sslcert_var)
    file.close()
    os.chmod("/client-cert.pem", stat.S_IRUSR)
    os.chmod("/client-cert.pem", stat.S_IWUSR)
    sslcert = "sslcert=/client-cert.pem"

    sslkey_var = os.environ.get('PG_SSLKEY')
    sslkey_var = sslkey_var.replace('@', '=')
    file = open("/client-key.pem", "w")
    file.write(sslkey_var)
    file.close()
    os.chmod("/client-key.pem", stat.S_IRUSR)
    os.chmod("/client-key.pem", stat.S_IWUSR)
    sslkey = "sslkey=/client-key.pem"

    hostaddr = "hostaddr={}".format(os.environ.get('PG_HOST'))
    user = "user=postgres"
    password = "password={}".format(os.environ.get('PG_PASSWORD'))
    dbname = "dbname=postgres"

    # Construct database connect string
    db_connect_string = " ".join([
        sslmode,
        sslrootcert,
        sslcert,
        sslkey,
        hostaddr,
        user,
        password,
        dbname
    ])

    return db_connect_string

def getInitialModel():
    # Initialize our default model.
    models = {
        "default": "distilled-bert",
        "models": [
            {
                "name": "distilled-bert",
                "tokenizer": "distilbert-base-uncased-distilled-squad",
                "model": "distilbert-base-uncased-distilled-squad",
                "pipeline": pipeline('question-answering',
                                     model="distilbert-base-uncased-distilled-squad",
                                     tokenizer="distilbert-base-uncased-distilled-squad")
            }
        ]
    }

    return models


def init_db(environment):
    print('Inside init_db' , environment)
    if environment == 'PROD':
        db_connect_string = getDBString_PROD()
        con = psycopg2.connect(db_connect_string)
    elif environment=='TEST':
        con = sql.connect("questionAnswerTest.db")
    elif environment=='LOCAL':
        con = sql.connect("questionAnswer.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS answers
                   (question text, context text, model text, answer text, timestamp int)''')
    return con


