# Read in the tranhist file and return the data with analysised data
import csv
import re
import json
from category import categoriesjson

#read in the csv file and return a dictionary storing the formatted data, a dictionary storing the months data 
# and a dictionary storing the summary of each month 
def setUp(filename="./statement/tranhist.csv"):
  #read in the csv file
  with open(filename,encoding="utf-8-sig") as csvfile:
    allData = csv.reader(csvfile)
    #row[0]: date row[1]: detail of payment   row[2]:amount
    date = []
    details = []
    amount = []
    for row in allData:
      date.append(row[0])
      details.append(row[1])
      amount.append(row[2])

  date.reverse()
  details.reverse()
  amount.reverse()  
  #divide details list into two list, store and ref
  store = []
  ref = []
  for row in details:
    spilted = re.split(r'\s{2,}', row)
    if len(spilted) == 3:
      store.append(spilted[0])
      ref.append(spilted[1]+", "+spilted[2])
    elif "************************************" in spilted[0]:
      store.append(spilted[1])
      ref.append(spilted[1])
    elif len(spilted) == 2:
      store.append(spilted[0])
      ref.append(spilted[1])
    elif "INT'L" in spilted[0]:
      store.append(spilted[1])
      temp = spilted[0]
      for n in range(2,len(spilted)):
        temp = temp + ", " +spilted[n] 
      ref.append(temp)
    else:
      store.append(row)
      ref.append("NA")

  #find the different month and the index of the first data of the month
  initialMonth = date[0].split('/')[1]
  initialMonthYear = date[0].split('/')[2]
  months = [(initialMonth+"-"+initialMonthYear,0)] #list to store the months and the start index in list
  firstIndex=0
  nextMonth = initialMonth
  for day in date:
    #reformat the date
    date[firstIndex]=day.split('/')[2]+"-"+day.split('/')[1]+"-"+day.split('/')[0]
    if day.split('/')[1] != nextMonth:
      nextMonth = day.split('/')[1]
      nextMonthYear = day.split('/')[2]
      months.append((nextMonth+"-"+nextMonthYear,firstIndex))
      firstIndex+=1
    else:
      firstIndex+=1

  #store everything in dictionary & calculate the summary of each month
  data = {}
  monthCount = 0
  totalAmount = 0
  creditAmount = 0
  debitAmount = 0
  amountDict = {}
  for (currentMonth,i) in months:
    data[currentMonth] = []
    #find the last index of this month
    try:
      (nextmonth,nextIndex) = months[monthCount+1]
    except:
      nextIndex = len(date)

    for n in range(i, nextIndex):
      #calculate the total,credit & debit amount
      pay_method="Card"
      category = "Others"
      try:
        currentAmount = float(amount[n])
      #handling the , in the amount
      except ValueError:
        amountList = amount[n].split(',')
        realAmount = ""
        for a in amountList:
          realAmount+=a
        currentAmount=float(realAmount)
        amount[n]=realAmount

      totalAmount+=currentAmount
      if currentAmount < 0:
        value = 'Debit'
        debitAmount+=currentAmount
      else:
        value = 'Credit'
        creditAmount+=currentAmount
      
      #finding the categories of the data
      # categoriesjson = readCategoriesJSON()
      for categoryjson in categoriesjson:
        for item in categoriesjson[categoryjson]:
          if item.upper() in store[n].upper():
            category = categoryjson

      #finding the paymeent method of the data      
      if "PAYPAL" in store[n]:
        pay_method="Paypal "+value

      #finding the categories of the data
      if "INTERNET TRANSFER" in ref[n]:
        category="Accounts Transfer, "+value
      if "ATM" in ref[n] or "CASH" in store[n]:
        category="ATM, "+value
      

      #store everything in the dict
      data[currentMonth].append({
        'Date': date[n],
        'Month': currentMonth,
        'Store': store[n],
        'Amount': amount[n],
        'Category':category,
        'Value': value,
        'Method':pay_method,
        'Ref': ref[n],
        'Excluded':False,
        'Notes':""
      })

    monthCount+=1
    #store the amount data of the month
    amountDict [currentMonth]= {
      'total': totalAmount,
      'debit': debitAmount,
      'credit': creditAmount
    }
    totalAmount=0
    creditAmount = 0
    debitAmount = 0

  return(data,months,amountDict)

#output the data dictionary as separated csv files
def outputDataSeperateCsv(data,month):
  for (month,i) in months:
    filename1 = "./analysised/"+month.split('-')[0]+"_"+month.split('-')[1]+"_analysised.csv"
    with open(filename1, mode='w+', newline='') as csv_file:
        fieldnames = ['Date','Month', 'Store', 'Amount','Category','Value','Method','Ref','Excluded','Notes']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for item in data[month]:
          writer.writerow(item)
  print("outputted the data as seperated csv files")
  
#outout the data dictionary as one csv file
def outputDataOneCsv(data,month):
  with open("./analysised/all_analysised.csv", mode='w+', newline='') as csv_file:
    fieldnames = ['Date','Month', 'Store', 'Amount','Category','Value','Method','Ref','Excluded','Notes']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for (month,i) in months:
      for item in data[month]:
        writer.writerow(item)
  print("outputted the data as one csv file")

#output as a JSON
def outputDataJson(data,filename='./analysised/data.json'):
  with open(filename, 'w+') as outfile:
    json.dump(data, outfile) 
  print("outputted the JSON file")

# readin the categories from the JSON file
def readCategoriesJSON(filename='./analysised/categories.json'):
  with open(filename) as json_file:
    categories = json.load(json_file)
  return categories

if __name__ == "__main__":
  (data,months,amountDict)=setUp()
  # print(data)
  # outputDataOneCsv(data,months)
  # outputDataSeperateCsv(data,months)
  # outputDataJson(data)
  # print(amountDict)
  