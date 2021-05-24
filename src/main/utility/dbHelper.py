import json
import sqlite3 as sql

class dbHelper:

    def initialSetUp(self):
        try:
            with sql.connect("questionAnswer.db") as con:
                cur = con.cursor()
                # Create the basic tables
                # AppLogger
                cur.execute(""" CREATE TABLE IF NOT EXISTS APPLOGGER (model_name text
                                         ,question_asked_time integer
                                         ,question_text text
                                         ,answer_sent_time integer
                                         ,answer_text text
                                         ,created_time integer
                                         ,created_by text
                                         ,modified_time integer
                                         ,modified_by text) """)

                # Models
                cur.execute(""" CREATE TABLE IF NOT EXISTS NLP_Models (name text,tokenizer text,model text)""")

                # QuestionAnswer
                cur.execute(
                    """ CREATE TABLE IF NOT EXISTS Question_Answer (modelName text,question text,context text,answer text,createdDate integer)""")

                con.commit()
                return "Initial DB setup completed"
        except:
            con.rollback()
            return "Exception occurred while initial DB setup"
        finally:
            con.close()

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


    def addModel(self,name, tokenizer, model):
        try:
            print('Inside dbHelper.addModel : ',model,tokenizer,name)
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


    def deleteModel(self,modelName):
        try:
            print('Inside dbHelper.deleteModel for model = ',modelName)
            with sql.connect("questionAnswer.db") as con:
                cur = con.cursor()

                cur.execute("DELETE FROM NLP_Models WHERE NAME = :modelName", {'modelName': modelName})
                con.commit()
                print('Inside dbHelper.deleteModel for model = ', modelName , "Model deleted successfully")
                return "Model deleted successfully"
        except:
            con.rollback()
            return "Exception occured while trying to delete model for model = "+modelName
        finally:
            con.close()


    def getRecentlyAnsweredQuestionsList(self,modelName, startTime, endTime):
        try:
            print('Inside dbHelper.getRecentlyAnsweredQuestionsList for model = ', modelName,' startTime = ' , startTime , ' endTime = ',endTime)
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

    def saveRecentlyAnsweredQuestion(self,modelName, question, context,answer,createdDate):
        try:
            print('Inside dbHelper.getRecentlyAnsweredQuestionsList for model = ', modelName, ' question = ',
                  question, ' context = ', context ,' answer = ',answer,'createdDate = ',createdDate)
            with sql.connect("questionAnswer.db") as con:

                cur = con.cursor()

                cur.execute(
                    "INSERT INTO Question_Answer VALUES (?,?,?,?,?)",
                                                {'modelName': modelName
                                                 ,'question':question
                                                ,'context': context
                                                , 'answer': answer
                                                 ,'createdDate':createdDate })
                print('Inside dbHelper.getRecentlyAnsweredQuestionsList ' , 'Data saved successfully')
                return "Data saved successfully"
        except:
            con.rollback()
            return "Exception occured while saving question answer data"
        finally:
            con.close()

    # Create method to store all the logs
    def saveDBLog(self):
        return "Log saved succesfully"
