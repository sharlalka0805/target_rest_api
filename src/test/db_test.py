# database testing scripts ##

import pandas as pd
from transformers.pipelines import pipeline
from flask import Flask
import sqlite3
from logger import logger


#if __name__ == '__main__':
    # app.run()

conn = sqlite3.connect('question_answer_log.db')

c = conn.cursor()

#c.execute("""CREATE TABLE logger (first  text, last text , Comments text)""")

#c.execute("INSERT INTO logger VALUES ('sbjksj','xsadsa','asdsd')")

#c.execute("Select * from logger")

#print(c.fetchall())

logger_1 = logger("Shipra","Harlalka")
logger_2 = logger('Esha','Kaushal')

c.execute("INSERT INTO logger VALUES (?,?,?)",(logger_1.first,logger_1.last,logger_1.comment))

c.execute("INSERT INTO logger VALUES (:first,:last,:comment)",{'first':logger_2.first,'last':logger_1.last
                                                               ,'comment':logger_1.comment})

# slect in SQLlite

c.execute("SELECT from logger WHERE first = ?" , ('Shipra',))

print(c.fetchall())

c.execute("Select * from logger where last = :last",{'last':'Shipra'})
conn.commit()

conn.close()

def insert_logger(logger_2):
    with conn:
        c.execute("INSERT INTO logger VALUES (:first,:last,:comment)", {'first': logger_2.first, 'last': logger_1.last
        , 'comment': logger_1.comment})


