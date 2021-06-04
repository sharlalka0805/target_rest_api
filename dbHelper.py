import os
import stat
import sys

import psycopg2

class dbHelper:

    def __init__(self):
        print('Inside dbhelper init')

        # Format DB connection information
        sslmode = "sslmode=verify-ca"
        hostaddr = "hostaddr={}".format(os.environ.get('PG_HOST'))
        user = "user=postgres"
        password = "password={}".format(os.environ.get('PG_PASSWORD'))
        dbname = "dbname=postgres"


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


        # Connect to your postgres DB
        self.con = psycopg2.connect(db_connect_string)


    def createDatabase(self):
        try:
                cur = self.con.cursor()
                # Create the basic tables
                # AppLogger
                cur.execute(""" CREATE TABLE IF NOT EXISTS APP_LOGGER (model_name text
                                         ,action_type text
                                         ,action_details text
                                         ,created_by text
                                         ,created_time integer )""")

                # Models
                cur.execute(""" CREATE TABLE IF NOT EXISTS NLP_Models (name text,tokenizer text,model text)""")

                # QuestionAnswer
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS Question_Answer (modelName text,question text,context text,
                    answer text,createdDate integer)""")

                self.con.commit()
                return "Initial DB setup completed"
        except Exception as err:
            print(err)
            self.con.rollback()
            return "Exception occurred while initial DB setup"
        finally:
            self.con.commit()

    def insertInitialData(self):
        try:
            print('Inside insertintialdata')

            cur = self.con.cursor()

            cur.execute(""" INSERT INTO NLP_Models VALUES('bert-base-multilingual-uncased','bert-base-multilingual-uncased','bert-base-multilingual-uncased' ) """)
            cur.execute(
                """ INSERT INTO NLP_Models VALUES('distilled-bert','distilbert-base-uncased-distilled-squad','distilbert-base-uncased-distilled-squad' ) """)
            cur.execute(
                """ INSERT INTO NLP_Models VALUES('deepset-roberta','deepset/roberta-base-squad2','deepset/roberta-base-squad2' ) """)

            self.con.commit()
            return "Initial DB setup completed"
        except Exception as err:
            print(err)
            self.con.rollback()
            return "Exception occurred while initial DB inserts"
        finally:
            self.con.commit()


    def listModels(self):
        try:
            cur = self.con.cursor()
            select_query = "SELECT * FROM NLP_Models"
            cur = self.con.execute(select_query)
            rows = cur.fetchall()
        except Exception as err:
            print(err)
            self.con.rollback()
            return "Exception occurred while fetching the list of models"
        finally:
            self.con.commit()
        return rows

    def addModel(self, name, tokenizer, model):
        try:
            print('Inside dbHelper.addModel : ', model, tokenizer, name)

            cur = self.con.cursor()
            # Introduce for in case you need to persist an ad-hoc lis
            cur.execute("INSERT INTO NLP_Models VALUES (?,?,?)", (name, tokenizer, model))
            self.con.commit()
            return "Model added successfully"
        except Exception as err:
            print(err)
            self.con.rollback()
            return "Exception occured while trying to add model"
        finally:
            self.con.commit()

    def deleteModel(self, modelName):
        try:
            print('Inside dbHelper.deleteModel for model = ', modelName)
            cur = self.con.cursor()

            cur.execute("DELETE FROM NLP_Models WHERE NAME = :modelName", {'modelName': modelName})
            self.con.commit()
            print('Inside dbHelper.deleteModel for model = ', modelName, "Model deleted successfully")
            return "Model deleted successfully"
        except Exception as err:
            print(err)
            self.con.rollback()
            return "Exception occured while trying to delete model for model = " + modelName
        finally:
            self.con.commit()

    def getRecentlyAnsweredQuestionsList(self, modelName, startTime, endTime):
        try:
            print('Inside dbHelper.getRecentlyAnsweredQuestionsList for model = ', modelName, ' startTime = ',
                  startTime, ' endTime = ', endTime)

            cur = self.con.cursor()

            if modelName !=" ":
                cur.execute(
                        "SELECT * FROM Question_Answer WHERE createdDate >= :startTime and createdDate <= :endTime and modelName = :modelName",
                        {'startTime': startTime, 'endTime': endTime, 'modelName': modelName})
            else:
                cur.execute(
                    "SELECT * FROM Question_Answer WHERE createdDate >= :startTime and createdDate <= :endTime",
                    {'startTime': startTime, 'endTime': endTime})

            rows = cur.fetchall()
            return rows
        except Exception as err:
            print(err)
            self.con.rollback()
            return "Exception occured while trying to fetch the list of recently answered questions"
        finally:
            self.con.commit()

    def saveRecentlyAnsweredQuestion(self, questionAnswer):
        try:
            print('Inside dbHelper.getRecentlyAnsweredQuestionsList for model = ', questionAnswer.modelName,
                  ' question = ',
                  questionAnswer.question, ' context = ', questionAnswer.context, ' answer = ', questionAnswer.answer,
                  'timeStamp = ', questionAnswer.timestamp)

            cur = self.con.cursor()

            cur.execute(
                    "INSERT INTO Question_Answer VALUES (:modelName,:question,:context,:answer,:timestamp)",
                    {'modelName': questionAnswer.modelName
                        , 'question': questionAnswer.question
                        , 'context': questionAnswer.context
                        , 'answer': questionAnswer.answer
                        , 'timestamp': questionAnswer.timestamp})
            print('Inside dbHelper.getRecentlyAnsweredQuestionsList ', 'Data saved successfully')
            return "Data saved successfully"
        except Exception as err:
            print(err)
            self.con.rollback()
            return "Exception occured while saving question answer data"
        finally:
            self.con.commit()

    # Create method to store all the logs
    def saveDBLog(self, appLogger):
        try:
            print('Inside dbHelper.saveDBLog')

            cur = self.con.cursor()

            cur.execute(
                    "INSERT INTO APP_LOGGER VALUES (?,?,?,?,?)",
                    {'modelName': appLogger.modelName
                        , 'action_type': appLogger.action_type
                        , 'action_details': appLogger.action_details
                        , 'created_by': appLogger.created_by
                        , 'created_time': appLogger.created_time})
            print('Inside dbHelper.saveDBLog ', 'Data saved successfully')
            return "Data saved successfully"
        except Exception as err:
            print(err)
            self.con.rollback()
            return "Exception occured while saving question answer data"
        finally:
            self.con.commit()

    # Method to get mode details
    def getModelDetails(self, modelName):
        print('Inside dbHelper.getModelDetails for modelName = ', modelName)
        try:
            cur = self.con.execute("SELECT * FROM NLP_Models WHERE model = :modelName", {'modelName': modelName})
            rows = cur.fetchall()
            return rows
        except Exception as err:
            print(err)
            self.con.rollback()
            return "Exception occurred while fetching the list of models"
        finally:
            self.con.commit()


    def getDBLogs(self):
        try:
            select_query = "SELECT * FROM Question_Answer order by createdDate desc"
            cur = self.con.execute(select_query)
            rows = cur.fetchall()
            return rows
        except:
            self.con.rollback()
            return "Exception occurred while fetching the list of models"
        finally:
            self.con.commit()

