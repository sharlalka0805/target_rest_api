# database testing scripts ##





from flask import Flask
import sqlite3

conn = sqlite3.connect('test_Database.db')

c = conn.cursor()

c.execute("""CREATE TABLE logger (first  text, last text , comments text)""")

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



conn = sqlite3.connect('questionAnswer.db')

c = conn.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS NLP_Models (name text,tokenizer text,model text)""")

c.execute(""" INSERT INTO NLP_Models(name,tokenizer,model) 
                                SELECT 'bert-base-multilingual-uncased'
                                        ,'bert-base-multilingual-uncased'
                                        ,'bert-base-multilingual-uncased' 
                                WHERE NOT EXISTS(
                                SELECT 1 FROM NLP_Models WHERE name = 'bert-base-multilingual-uncased'); """)

c.execute("Select * from NLP_Models")

print(c.fetchall())