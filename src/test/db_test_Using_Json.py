import sqlite3 as sql
import requests,pprint,json

print(sql.version)

conn = sql.connect('testDatabase.db')
cursor = conn.cursor()

countries_api_res = requests.get('http://api.worldbank.org/countries?format=json&per_page=100')
countries = countries_api_res.json()[1]

print(countries)
pprint.pprint(countries)

# Create a table
cursor.execute("CREATE TABLE countries (id varchar(3), data json)")

#Insert Values in the  table
for country in countries:
   cursor.execute("insert into countries values (?, ?)",[country['id'], json.dumps(country)])
   conn.commit()

#Select Data from tables
data = cursor.execute(''' select json_extract(data , '$.name') from countries''').fetchmany(5)

type(data)
