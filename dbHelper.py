import sqlite3 as sql

class dbHelper:

    def createDatabase(self):
        try:
            with sql.connect("questionAnswer.db") as con:
                cur = con.cursor()
                # Create the basic tables
                # AppLogger
                cur.execute(""" CREATE TABLE IF NOT EXISTS APP_LOGGER (model_name text
                                         ,action_type text
                                         ,action_details text
                                         ,created_by text
                                         ,created_time integer """)

                # Models
                cur.execute(""" CREATE TABLE IF NOT EXISTS NLP_Models (name text,tokenizer text,model text)""")

                # QuestionAnswer
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS Question_Answer (modelName text,question text,context text,
                    answer text,createdDate integer)""")

                con.commit()
                return "Initial DB setup completed"
        except:
            con.rollback()
            return "Exception occurred while initial DB setup"
        finally:
            con.close()

    def insertInitialData(self):
        try:
            print('Inside insertintialdata')

            with sql.connect("questionAnswer.db") as con:
                cur = con.cursor()
                # Create the basic tables

                cur.execute(""" INSERT INTO NLP_Models VALUES(name,tokenizer,model) 
                                SELECT 'bert-base-multilingual-uncased'
                                        ,'bert-base-multilingual-uncased'
                                        ,'bert-base-multilingual-uncased' 
                                WHERE NOT EXISTS(
                                SELECT 1 FROM NLP_Models WHERE name = 'bert-base-multilingual-uncased'); """)

                con.commit()
                return "Initial DB setup completed"
        except:
            con.rollback()
            return "Exception occurred while initial DB inserts"
        finally:
            con.close()

    # Create method to upload default data in NLP Models table using XML

    def listModels(self):
        try:
            with sql.connect("questionAnswer.db") as con:
                con.row_factory = sql.Row
                select_query = "SELECT * FROM NLP_Models"
                cur = con.execute(select_query)
                rows = cur.fetchall()
        except:
            con.rollback()
            return "Exception occurred while fetching the list of models"
        finally:
            con.close()
        return rows

    def addModel(self, name, tokenizer, model):
        try:
            print('Inside dbHelper.addModel : ', model, tokenizer, name)
            with sql.connect("questionAnswer.db") as con:
                cur = con.cursor()
                # Introduce for in case you need to persist an ad-hoc lis
                cur.execute("INSERT INTO NLP_Models VALUES (?,?,?)", (name, tokenizer, model))
                con.commit()
                return "Model added successfully"
        except:
            con.rollback()
            return "Exception occured while trying to add model"
        finally:
            con.close()

    def deleteModel(self, modelName):
        try:
            print('Inside dbHelper.deleteModel for model = ', modelName)
            with sql.connect("questionAnswer.db") as con:
                cur = con.cursor()

                cur.execute("DELETE FROM NLP_Models WHERE NAME = :modelName", {'modelName': modelName})
                con.commit()
                print('Inside dbHelper.deleteModel for model = ', modelName, "Model deleted successfully")
                return "Model deleted successfully"
        except:
            con.rollback()
            return "Exception occured while trying to delete model for model = " + modelName
        finally:
            con.close()

    def getRecentlyAnsweredQuestionsList(self, modelName, startTime, endTime):
        try:
            print('Inside dbHelper.getRecentlyAnsweredQuestionsList for model = ', modelName, ' startTime = ',
                  startTime, ' endTime = ', endTime)
            with sql.connect("questionAnswer.db") as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                cur.execute(
                    "SELECT * FROM Question_Answer WHERE createdDate >= :startTime and createdDate <= :endTime and modelName = :modelName",
                    {'startTime': startTime, 'endTime': endTime, 'modelName': modelName})

                rows = cur.fetchall()
                return rows
        except:
            con.rollback()
            return "Exception occured while trying to fetch the list of recently answered questions"
        finally:
            con.close()

    def saveRecentlyAnsweredQuestion(self, questionAnswer):
        try:
            print('Inside dbHelper.getRecentlyAnsweredQuestionsList for model = ', questionAnswer.modelName,
                  ' question = ',
                  questionAnswer.question, ' context = ', questionAnswer.context, ' answer = ', questionAnswer.answer,
                  'timeStamp = ', questionAnswer.timestamp)
            with sql.connect("questionAnswer.db") as con:

                cur = con.cursor()

                cur.execute(
                    "INSERT INTO Question_Answer VALUES (?,?,?,?,?)",
                    {'modelName': questionAnswer.modelName
                        , 'question': questionAnswer.question
                        , 'context': questionAnswer.context
                        , 'answer': questionAnswer.answer
                        , 'timestamp': questionAnswer.timestamp})
                print('Inside dbHelper.getRecentlyAnsweredQuestionsList ', 'Data saved successfully')
                return "Data saved successfully"
        except:
            con.rollback()
            return "Exception occured while saving question answer data"
        finally:
            con.close()

    # Create method to store all the logs
    def saveDBLog(self, appLogger):
        try:
            print('Inside dbHelper.saveDBLog')
            with sql.connect("questionAnswer.db") as con:

                cur = con.cursor()

                cur.execute(
                    "INSERT INTO APP_LOGGER VALUES (?,?,?,?,?)",
                    {'modelName': appLogger.modelName
                        , 'action_type': appLogger.action_type
                        , 'action_details': appLogger.action_details
                        , 'created_by': appLogger.created_by
                        , 'created_time': appLogger.created_time})
                print('Inside dbHelper.saveDBLog ', 'Data saved successfully')
                return "Data saved successfully"
        except:
            con.rollback()
            return "Exception occured while saving question answer data"
        finally:
            con.close()

    # Method to get mode details
    def getModelDetails(self, modelName):
        print('Inside dbHelper.getModelDetails for modelName = ', modelName)
        try:
            with sql.connect("questionAnswer.db") as con:
                con.row_factory = sql.Row
                cur = con.execute("SELECT * FROM NLP_Models WHERE model = :modelName", {'modelName': modelName})
                rows = cur.fetchall()
                return rows
        except:
            con.rollback()
            return "Exception occurred while fetching the list of models"
        finally:
            con.close()


    def getDBLogs(self):
        try:
            with sql.connect("questionAnswer.db") as con:
                con.row_factory = sql.Row
                select_query = "SELECT * FROM Question_Answer order by createdDate desc"
                cur = con.execute(select_query)
                rows = cur.fetchall()
                return rows
        except:
            con.rollback()
            return "Exception occurred while fetching the list of models"
        finally:
            con.close()

