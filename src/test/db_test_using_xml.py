# database testing scripts ##
import xml.etree.ElementTree
import sqlite3 as sql
import os

conn = sql.connect('test_db.db')

def insert_person(db_conn, person_id, first_name, last_name, profession):
     curs = db_conn.cursor()
     curs.execute("insert into person values (?, ?, ?, ?)",
     (person_id, first_name, last_name, profession))
     db_conn.commit()

def person_data_from_element(element):
     first = element.find("firstName").text
     last = element.find("lastName").text
     profession = element.find("profession").text
     return first, last, profession

if __name__ == "__main__":
     conn = sql.connect("test_db.db")
     curs = conn.cursor()

     curs.execute(""" create table if not exists person (
                               person_id text,
                               first_name text,
                               last_name text,
                               profession text
                              );""")
     print(os.getcwd())
     people = xml.etree.ElementTree.parse("people_data.xml")
     persons = people.findall("person")
     for index, element in enumerate(persons):
         first, last, profession = person_data_from_element(element)
         insert_person(conn, index, first, last, profession)

     curs.execute("SELECT * from person")
     print(curs.fetchall())




