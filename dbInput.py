# Connection with the database. Do stuff like creating the table and inserting data into the table
from readData import setUp
import mysql.connector as mysql
from dbconfig import dbConfig


#CREATE TABLE                                                                                                                     
# mycursor.execute("CREATE TABLE analysised (id INT AUTO_INCREMENT PRIMARY KEY, Date VARCHAR(255) NOT NULL, Month VARCHAR(255) NOT NULL, Store VARCHAR(255) NOT NULL, Amount FLOAT NOT NULL, Category VARCHAR(255) NOT NULL,Value VARCHAR(255) NOT NULL, Payment_Method VARCHAR(255) NOT NULL,Ref VARCHAR(255), Notes VARCHAR(255),Excluded BOOLEAN);")

table = "analysised" #set this to the table name u created
#get the data from the setUp method of readData.py and save it to the dbInput list
def getdbInput(data,months):
  dbInput = []
  for (month,i) in months:
    for item in data[month]:
      temp=(item['Date'],item['Month'],item['Store'],item['Amount'],item['Category'],item['Value'],item['Method'],item['Ref'],item['Notes'],item['Excluded'])
      dbInput.append(temp)

  return dbInput

#insert all rows in the dbInput list to the database with the given cursor and connection
def insert(dbInput,mycursor,conn):
  sql = "INSERT INTO "+table+"(Date, Month,Store,Amount,Category,Value,Payment_Method,Ref,Notes,Excluded) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"

  mycursor.executemany(sql, dbInput)

  conn.commit()

  print(mycursor.rowcount, "was inserted.")


if __name__ == "__main__":

  conn = mysql.connect(**dbConfig)
  mycursor = conn.cursor()

  #insert
  (data,months,amountDict)=setUp()
  dbInput = getdbInput(data,months)
  insert(dbInput,mycursor,conn)

  mycursor.close
  conn.close
