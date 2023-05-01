from flask import Flask, render_template, request, redirect
from . import home
import sqlite3
import os
from .csv_input.db_conf import DBCONF
from .csv_input.db_input import importToDb
from .csv_input.read_data import generateDict

table = DBCONF['table']
dbName = DBCONF['dbName']
upload_folder = "./uploads"

#region Index Page
'''
	index/home page
	show all the option of months from database and redirect to the month.html or breakdown.html based on the selected month
'''
@home.route("/")
def homepage():
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT DISTINCT Month FROM {table};")
    months = cursor.fetchall()
    
    cursor.close
    conn.close
    return render_template("index.html",months=months)
#endregion

#region month Page
'''
	handle the get request from the index page 
	-> show all the records of the given month 
'''
@home.route("/month")
def month():
	selectedMonth = request.args['month']

	conn = sqlite3.connect(dbName)
	mycursor = conn.cursor()

	#get all records for the selectedMonth
	sql= f"SELECT * FROM {table} WHERE Month = '{selectedMonth}' ORDER BY Date ASC;"
	mycursor.execute(sql)
	allResult = mycursor.fetchall()

	#get debit records for the selectedMonth
	sql= f"SELECT * FROM {table} WHERE Month= '{selectedMonth}' AND AMOUNT <0 ORDER BY Date ASC;"
	mycursor.execute(sql)
	debitResult = mycursor.fetchall()

	#get credit records for the selectedMonth
	sql= f"SELECT * FROM {table} WHERE Month= '{selectedMonth}' AND AMOUNT >0 ORDER BY Date ASC;"
	mycursor.execute(sql)
	creditResult = mycursor.fetchall()

	#get the summary list (0:debit total; 1: credit total; 2: balance;)
	summary=[]
	sql= f"SELECT SUM(Amount) FROM {table} WHERE Month= '{selectedMonth}' AND AMOUNT < 0 AND Excluded = false;"
	mycursor.execute(sql)
	summary.append(mycursor.fetchall()[0][0])

	sql= f"SELECT SUM(Amount) FROM {table} WHERE Month= '{selectedMonth}' AND AMOUNT > 0 AND Excluded = false;"
	mycursor.execute(sql)
	summary.append(mycursor.fetchall()[0][0])

	sql= f"SELECT SUM(Amount) FROM {table} WHERE Month= '{selectedMonth}' AND Excluded = false;"
	mycursor.execute(sql)
	balance = mycursor.fetchall()[0][0]
	summary.append(balance)

	mycursor.close
	conn.close
	return render_template("month.html",allResult=allResult,debitResult=debitResult,creditResult=creditResult,month=selectedMonth,summary=summary)
#endregion

#region breakdown page
'''
	handle the get request from index.html 
	-> show the breakdown of records based on categories
'''
@home.route('/breakdown')
def breakdown():
	month = request.args['month']
	conn = sqlite3.connect(dbName)
	mycursor = conn.cursor()

	#credit Data
	#get all categories of the credit data
	sql= f"SELECT DISTINCT Category FROM {table} WHERE Month= '{month}' AND Excluded = False AND Amount > 0;"
	mycursor.execute(sql)
	creditCategories = mycursor.fetchall()

	#get sum of each category and add them to the creditData list
	creditData = []
	for category in creditCategories:
		sql= f"SELECT SUM(Amount) FROM {table} WHERE Month= '{month}' AND Category = '{category[0]}' AND Excluded = False AND Amount > 0;"
		mycursor.execute(sql)
		categoryData = mycursor.fetchall()
		creditData.append([category[0],categoryData[0][0]])

	#get all credit record grouped by categories
	sql= f"SELECT * FROM {table} WHERE Month = '{month}' AND Excluded = False AND Amount > 0 order by category;"
	mycursor.execute(sql)
	creditRecords = mycursor.fetchall()


	#Debit Data
	#get all categories of the credit data
	sql= f"SELECT DISTINCT Category FROM {table} WHERE Month= '{month}' AND Excluded = False AND Amount < 0;"
	mycursor.execute(sql)
	debitCategories = mycursor.fetchall()

	#get sum of each category and add them to the debitData list
	debitData = []
	for category in debitCategories:
		sql= f"SELECT SUM(Amount) FROM {table} WHERE Month= '{month}' AND Category = '{category[0]}' AND Excluded = False AND Amount < 0;"
		mycursor.execute(sql)
		categoryData = mycursor.fetchall()
		debitData.append([category[0],(-categoryData[0][0])])
	
	#get all debit records grouped by category
	sql= f"SELECT * FROM {table} WHERE Month = '{month}' AND Excluded = False AND Amount < 0 order by category;"
	mycursor.execute(sql)
	debitRecords = mycursor.fetchall()


	#get the summary list (0:debit total; 1: credit total; 2: balance;)
	summary=[]
	#debit
	sql= f"SELECT SUM(Amount) FROM {table} WHERE Month= '{month}' AND AMOUNT < 0 AND Excluded = false;"
	mycursor.execute(sql)
	summary.append(mycursor.fetchall()[0][0])

	#credit
	sql= f"SELECT SUM(Amount) FROM {table} WHERE Month= '{month}' AND AMOUNT > 0 AND Excluded = false;"
	mycursor.execute(sql)
	summary.append(mycursor.fetchall()[0][0])

	#total
	sql= f"SELECT SUM(Amount) FROM {table} WHERE Month= '{month}' AND Excluded = false;"
	mycursor.execute(sql)
	summary.append(mycursor.fetchall()[0][0])


	#store analysis debit
	sql= f"SELECT store,SUM(Amount) FROM {table} WHERE Month = '{month}' AND Excluded = False AND Amount < 0 group by store;"
	mycursor.execute(sql)
	storeDebit = mycursor.fetchall()

	#store analysis credit
	sql= f"SELECT store,SUM(Amount) FROM {table} WHERE Month = '{month}' AND Excluded = False AND Amount > 0 group by store;"
	mycursor.execute(sql)
	storeCredit = mycursor.fetchall()

	mycursor.close
	conn.close
	return render_template("breakdown.html",creditData=creditData,debitData=debitData,debitCategories=debitCategories,month=month,creditRecords=creditRecords,debitRecords=debitRecords,summary=summary,storeDebit=storeDebit,storeCredit=storeCredit)
#endregion

#region update/delete a single record recognized by id
'''
	Post the data in edit form (edit.html) to database
'''
@home.route('/update',methods=["POST"])
def update():
	conn = sqlite3.connect(dbName)
	mycursor = conn.cursor()

	sql=f"UPDATE {table} SET Date = ?,Month = ?,Store=?,Amount = ?, Category = ?,Bank = ?, Notes = ?, Excluded=? WHERE id = ?;"
	values= (request.form['date'],request.form['month'],request.form['store'],request.form['amount'],request.form['category'],request.form['bank'],request.form['notes'],eval(request.form['radio']),request.form['id'])
	
	mycursor.execute(sql, values)
	conn.commit()

	mycursor.close
	conn.close
	return redirect(request.referrer)

'''
	handle the request from edit.html 
	-> delete the record from database
'''
@home.route('/deleteRecord/<int:id>')
def deleteRecord(id):
	conn = sqlite3.connect(dbName)
	mycursor = conn.cursor()

	sql= f"DELETE FROM {table} WHERE id = {id}"

	mycursor.execute(sql)
	conn.commit()

	affectedRows = mycursor.rowcount
	mycursor.close
	conn.close
	return render_template("success.html",affectedRows=affectedRows,id=id, addNewLines=False)
#endregion

#region add record
'''
	form for adding new record
'''
@home.route('/newRecordForm')
def newRecordForm():
	conn = sqlite3.connect(dbName)
	mycursor = conn.cursor()

	#get all existing categories
	sql= f"SELECT DISTINCT Category FROM {table};"
	mycursor.execute(sql)
	categories = mycursor.fetchall()

	return render_template('newRecordForm.html',categories=categories)

'''
	handle the post request from the newRecordForm page
	actually sending the insert request to the database
'''
@home.route('/addRecord',methods=["POST"])
def addRecord():
	conn = sqlite3.connect(dbName)
	mycursor = conn.cursor()

	sql= f"INSERT INTO {table} (Date, Month, Store, Amount, Category, Bank, Notes, Excluded) VALUES ('{request.form['date']}','{request.form['month']}','{request.form['store']}',{request.form['amount']},'{request.form['categories']}','{request.form['bank']}','{request.form['notes']}',{eval(request.form['radio'])});"

	mycursor.execute(sql)
	conn.commit()
	affectedRows = mycursor.rowcount

	mycursor.close
	conn.close
	return render_template("success.html",affectedRows=affectedRows, addNewLines=True)
#endregion

#region saving page
'''
	page to show bills, saving and salary
'''
@home.route('/saving')
def saving():
	conn = sqlite3.connect(dbName)
	mycursor = conn.cursor()

	#get grouped saving records
	sql= f"SELECT Month, SUM(Amount) FROM {table} WHERE Category = 'Saving' GROUP BY Month ORDER BY Month;"
	mycursor.execute(sql)
	groupedSavings = mycursor.fetchall()

	#get the sum of saving
	savingSum = 0
	for s in groupedSavings:
		savingSum += s[1]
	
	#get saving records
	sql= f"SELECT Date, Month, Store, Amount, Notes FROM {table} WHERE Category = 'Saving' ORDER BY Month;"
	mycursor.execute(sql)
	savingsRecord = mycursor.fetchall()

	#get all salary records
	sql= f"SELECT Month,Store,Amount,Notes FROM {table} WHERE Category = 'Salary';"
	mycursor.execute(sql)
	salary = mycursor.fetchall()

	#get all bill records
	sql= f"SELECT Month,Store,Amount,Notes FROM {table} WHERE Category = 'Bills' ORDER BY Month;"
	mycursor.execute(sql)
	bills = mycursor.fetchall()
	
	return render_template('saving.html',groupedSavings=groupedSavings,salary=salary,bills=bills, sums=round(savingSum,2), savingsRecord=savingsRecord)
#endregion

@home.route("/db_input")
def dbInput():
    bank = request.args['bank']
    filename = request.args['filename']

    lineCount = inputFileToDb(bank, filename)
    return render_template("dbInput.html", lineCount=lineCount)

def inputFileToDb(bank, filepath):
	conn = sqlite3.connect(dbName)
	mycursor = conn.cursor()
	
	(data,months)= generateDict(bank, filepath)
	lineCount = importToDb(data,months,mycursor,conn)
	mycursor.close
	conn.close
	return lineCount

@home.route("/select_file")
def selectFile():
    return render_template("selectFile.html")

@home.route("/uploader", methods = ['POST'])
def uploader():
    f = request.files['file']
    filepath = os.path.join(upload_folder, f.filename)
    f.save(filepath) 
    
    lineCount = inputFileToDb("HSBC", filepath)
    return render_template("success.html", affectedRows=lineCount, addNewLines =True)