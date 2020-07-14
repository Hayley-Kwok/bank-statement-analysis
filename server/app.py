# Server File
from flask import Flask, render_template, request
import mysql.connector as mysql
from dbconfig import dbConfig #a dictionary that store all the connection credientals 

app = Flask(__name__) 

#set this variable to be the name of the table that store all of the data
table = "analysised"

#index/home page
#show all the option of months from database and redirect to the month.html or breakdown.html based on the selected month
@app.route("/")
def home():
	conn =mysql.connect(**dbConfig)
	mycursor = conn.cursor()

	mycursor.execute("SELECT DISTINCT Month FROM "+table+";")
	months = mycursor.fetchall()

	mycursor.close
	conn.close
	return render_template("index.html",months=months)

#handle the get request from the index page
#show all the records of the given month 
@app.route("/month")
def month():
	selectedMonth = request.args['month']
	sqlMonth = (selectedMonth,)

	conn = mysql.connect(**dbConfig)
	mycursor = conn.cursor()

	#get all records for the selectedMonth
	sql="SELECT * FROM "+table+" WHERE Month= %s"
	mycursor.execute(sql,sqlMonth)
	allResult = mycursor.fetchall()

	#get debit records for the selectedMonth
	sql="SELECT * FROM "+table+" WHERE Month= %s AND AMOUNT <0;"
	mycursor.execute(sql,sqlMonth)
	debitResult = mycursor.fetchall()

	#get credit records for the selectedMonth
	sql="SELECT * FROM "+table+" WHERE Month= %s AND AMOUNT >0;"
	mycursor.execute(sql,sqlMonth)
	creditResult = mycursor.fetchall()

	#get the summary list (0:debit total; 1: credit total; 2: balance;)
	summary=[]
	sql="SELECT SUM(Amount) FROM "+table+" WHERE Month= %s AND AMOUNT < 0 AND Excluded = false;"
	mycursor.execute(sql,sqlMonth)
	summary.append(mycursor.fetchall()[0][0])

	sql="SELECT SUM(Amount) FROM "+table+" WHERE Month= %s AND AMOUNT > 0 AND Excluded = false;"
	mycursor.execute(sql,sqlMonth)
	summary.append(mycursor.fetchall()[0][0])

	sql="SELECT SUM(Amount) FROM "+table+" WHERE Month= %s AND Excluded = false;"
	mycursor.execute(sql,sqlMonth)
	summary.append(mycursor.fetchall()[0][0])

	mycursor.close
	conn.close
	return render_template("month.html",allResult=allResult,debitResult=debitResult,creditResult=creditResult,month=selectedMonth,summary=summary)

#handle get request from the month.html
#show the form for updating or deleting record with the given id
@app.route('/<int:id>')
def edit(id):
	conn = mysql.connect(**dbConfig)
	mycursor = conn.cursor()

	#get the corresponding record from database
	sql="SELECT * FROM "+table+" WHERE id = %s"
	sqlid = (id,)
	mycursor.execute(sql,sqlid)
	selectedResult = mycursor.fetchall()

	mycursor.close
	conn.close
	
	return render_template("edit.html",result=selectedResult,id=id)

#handle the post request from edit.html
#update the record from database
@app.route('/update',methods=["POST"])
def update():
	conn = mysql.connect(**dbConfig)
	mycursor = conn.cursor()

	condition="UPDATE "+table+" SET Date = %s,Month = %s,Store=%s,Amount = %s, Category = %s,Value = %s,Payment_Method = %s, Ref = %s, Notes = %s, Excluded=%s WHERE id = %s;"
	val = (request.form['date'],request.form['month'],request.form['store'],request.form['amount'],request.form['category'],request.form['value'],request.form['method'],request.form['ref'],request.form['notes'],eval(request.form['radio']),request.form['id'])
	mycursor.execute(condition,val)
	conn.commit()

	affectedRows = mycursor.rowcount
	mycursor.close
	conn.close
	return render_template("success.html",affectedRows=affectedRows,id=request.form['id'])

#handle the get request from edit.html
#delete the record from database
@app.route('/deleteRecord/<int:id>')
def deleteRecord(id):
	conn = mysql.connect(**dbConfig)
	mycursor = conn.cursor()

	condition= "DELETE FROM "+table+" WHERE id = %s"
	val = (id,)
	mycursor.execute(condition,val)
	conn.commit()

	affectedRows = mycursor.rowcount
	mycursor.close
	conn.close
	return render_template("success.html",affectedRows=affectedRows,id=id)

#handle the get request from index.html 
#show the breakdown of records based on categories
@app.route('/breakdown')
def breakdown():
	month = request.args['month']
	sqlMonth = (month,)
	conn = mysql.connect(**dbConfig)
	mycursor = conn.cursor()

	#credit Data
	#get all categories of the credit data
	sql="SELECT DISTINCT Category FROM "+table+" WHERE Month= %s AND Excluded = False AND Amount > 0;"
	mycursor.execute(sql,sqlMonth)
	creditCategories = mycursor.fetchall()

	#get sum of each category and add them to the creditData list
	creditData = []
	for category in creditCategories:
		sql="SELECT SUM(Amount) FROM "+table+" WHERE Month= %s AND Category = %s AND Excluded = False AND Amount > 0;"
		val = (month,category[0])
		mycursor.execute(sql,val)
		categoryData = mycursor.fetchall()
		creditData.append([category[0],categoryData[0][0]])

	#get all credit record grouped by categories
	sql="SELECT * FROM "+table+" WHERE Month = %s AND Excluded = False AND Amount > 0 order by category;"
	mycursor.execute(sql,sqlMonth)
	creditRecords = mycursor.fetchall()


	#Debit Data
	#get all categories of the credit data
	sql="SELECT DISTINCT Category FROM "+table+" WHERE Month= %s AND Excluded = False AND Amount < 0;"
	mycursor.execute(sql,sqlMonth)
	debitCategories = mycursor.fetchall()

	#get sum of each category and add them to the debitData list
	debitData = []
	for category in debitCategories:
		sql="SELECT SUM(Amount) FROM "+table+" WHERE Month= %s AND Category = %s AND Excluded = False AND Amount < 0;"
		val = (month,category[0])
		mycursor.execute(sql,val)
		categoryData = mycursor.fetchall()
		debitData.append([category[0],(-categoryData[0][0])])
	
	#get all debit records grouped by category
	sql="SELECT * FROM "+table+" WHERE Month = %s AND Excluded = False AND Amount < 0 order by category;"
	mycursor.execute(sql,sqlMonth)
	debitRecords = mycursor.fetchall()


	#get the summary list (0:debit total; 1: credit total; 2: balance;)
	summary=[]
	#debit
	sql="SELECT SUM(Amount) FROM "+table+" WHERE Month= %s AND AMOUNT < 0 AND Excluded = false;"
	mycursor.execute(sql,sqlMonth)
	summary.append(mycursor.fetchall()[0][0])

	#credit
	sql="SELECT SUM(Amount) FROM "+table+" WHERE Month= %s AND AMOUNT > 0 AND Excluded = false;"
	mycursor.execute(sql,sqlMonth)
	summary.append(mycursor.fetchall()[0][0])

	#total
	sql="SELECT SUM(Amount) FROM "+table+" WHERE Month= %s AND Excluded = false;"
	mycursor.execute(sql,sqlMonth)
	summary.append(mycursor.fetchall()[0][0])


	#store analysis debit
	sql="SELECT store,SUM(Amount) FROM "+table+" WHERE Month = %s AND Excluded = False AND Amount < 0 group by store;"
	mycursor.execute(sql,sqlMonth)
	storeDebit = mycursor.fetchall()

	#store analysis credit
	sql="SELECT store,SUM(Amount) FROM "+table+" WHERE Month = %s AND Excluded = False AND Amount > 0 group by store;"
	mycursor.execute(sql,sqlMonth)
	storeCredit = mycursor.fetchall()

	mycursor.close
	conn.close
	return render_template("breakdown.html",creditData=creditData,debitData=debitData,debitCategories=debitCategories,month=month,creditRecords=creditRecords,debitRecords=debitRecords,summary=summary,storeDebit=storeDebit,storeCredit=storeCredit)

#form for adding new record
@app.route('/newRecordForm')
def newRecordForm():
	conn = mysql.connect(**dbConfig)
	mycursor = conn.cursor()

	#get all existing categories
	sql="SELECT DISTINCT Category FROM "+table+";"
	mycursor.execute(sql)
	categories = mycursor.fetchall()

	return render_template('newRecordForm.html',categories=categories)

#handle the post request from the newRecordForm page
#actually sending the insert request to the database
@app.route('/addRecord',methods=["POST"])
def addRecord():
	conn = mysql.connect(**dbConfig)
	mycursor = conn.cursor()

	condition="INSERT INTO "+table+" (Date, Month, Store, Amount, Category,Value,Payment_Method, Ref, Notes, Excluded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	val = (request.form['date'],request.form['month'],request.form['store'],request.form['amount'],request.form['categories'],request.form['value'],request.form['methods'],request.form['ref'],request.form['notes'],eval(request.form['radio']))
	mycursor.execute(condition,val)
	conn.commit()
	affectedRows = mycursor.rowcount

	mycursor.close
	conn.close
	return render_template("success.html",affectedRows=affectedRows)
	
#page to show bills, saving and salary
@app.route('/saving')
def saving():
	conn = mysql.connect(**dbConfig)
	mycursor = conn.cursor()

	#get all saving records
	sql="SELECT Month,Amount FROM "+table+" WHERE Category = 'Saving';"
	mycursor.execute(sql)
	savings = mycursor.fetchall()

	#get the sum of saving
	savingSum = 0
	for s in savings:
		savingSum += s[1]
	
	#get all salary records
	sql="SELECT Month,Store,Amount,Notes FROM "+table+" WHERE Category = 'Salary';"
	mycursor.execute(sql)
	salary = mycursor.fetchall()

	#get all bill records
	sql="SELECT Month,Store,Amount,Notes FROM "+table+" WHERE Category = 'Bills';"
	mycursor.execute(sql)
	bills = mycursor.fetchall()
	
	return render_template('saving.html',savings=savings,salary=salary,bills=bills, sums=round(savingSum,2))

#error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',error="Page Not Found",message="What you are finding is not here."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html',error="Error Occuried",message="An error occuried."), 500

def handle_bad_request(e):
    return render_template('error.html',error="Error Occuried",message="An error occuried."), 400
app.register_error_handler(404, handle_bad_request)

app.run(debug=True)