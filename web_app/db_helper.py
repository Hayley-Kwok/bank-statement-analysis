#import csv files to the db 
# csv file formatted like below
# 1479,2021-05-31,2021-06,"Aldi",-10.09,Grocery,Starling,,0

import csv
import sqlite3
from app.home.csv_input.db_conf import DBCONF

table = DBCONF["table"]

# Migration function
def importFromCsv(filename):
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    with open(filename, encoding="utf-8-sig") as csvfile:
        allData = csv.reader(csvfile)

        for row in allData:
            condition= f'INSERT INTO {table} (id,Date, Month, Store, Amount, Category, Bank, Notes, Excluded) VALUES ("{row[0]}","{row[1]}","{row[2]}","{row[3]}",{row[4]},"{row[5]}","{row[6]}","{row[7]}", {row[8]})'
            cursor.execute(condition)
        
    conn.commit()
    conn.close()

def createAnalysisedTable():
	conn = sqlite3.connect(DBCONF["dbName"])

	cursor = conn.cursor()
	cursor.execute(f"DROP TABLE IF EXISTS {table}")
	#Creating table as per requirement
	sql ='''CREATE TABLE "analysised" (
	"id"	INTEGER,
	"Date"	TEXT,
	"Month"	TEXT,
	"Store"	TEXT,
	"Amount"	NUMERIC,
	"Category"	TEXT,
	"Bank"	TEXT,
	"Notes"	TEXT,
	"Excluded"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
)'''
	cursor.execute(sql)
	conn.commit()
	conn.close()

def checkIfTableExist(tableName = table):
    conn = sqlite3.connect(DBCONF["dbName"])
    cursor = conn.cursor()
    sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';"
    cursor.execute(sql)
    allResult = cursor.fetchall()
     
    cursor.close
    conn.close
    return allResult

def deleteTable():
     conn = sqlite3.connect(DBCONF["dbName"])
     cursor = conn.cursor()
     cursor.execute(f"DROP TABLE IF EXISTS {table}")
     
     cursor.close
     conn.close

if __name__ == "__main__":
    # createTable()
	deleteTable()
	print(len(checkIfTableExist())) 
    # importFromCsv(filename="C:\\Users\\wingk\\Downloads\\analysised_mysql.csv")
    # importFromCsv(filename="C:\\Users\\wingk\\Downloads\\analysised_mysql_2.csv")
