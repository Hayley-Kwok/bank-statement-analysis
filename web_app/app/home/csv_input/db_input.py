# Connection with the database. Do stuff like inserting data into the table
from .read_data import generateDictHSBC, generateDictStarling
from .db_conf import DBCONF as DBCONF
import sqlite3

table = DBCONF['table']

def importToDb(data, months, cursor, conn):
  dbInput = getdbInput(data,months)
  return insert(dbInput, cursor, conn)

def getdbInput(data,months):
  """
  Get the data from the setUp method of readData.py and save it to the dbInput list
  """
  dbInput = []
  for (month,i) in months:
    for item in data[month]:
      temp=(item['Date'],item['Month'],item['Store'],item['Amount'],item['Category'],item['Bank'],item['Notes'],item['Excluded'])
      dbInput.append(temp)

  return dbInput

def insert(dbInput,mycursor,conn):
  """
  Insert all rows in the dbInput list to the database with the given cursor and connection
  """
  sql = f"INSERT INTO {table} (Date,Month,Store,Amount,Category,Bank,Notes,Excluded) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

  mycursor.executemany(sql, dbInput)

  conn.commit()

  return mycursor.rowcount

if __name__ == "__main__":

  conn = sqlite3.connect(DBCONF['dbName'])
  mycursor = conn.cursor()
  
  #put the data from ./statement/tranhist.csv (default value) into the database 
  (data,months)=generateDictStarling()

  dbInput = getdbInput(data,months)
  insert(dbInput,mycursor,conn)

  mycursor.close
  conn.close
