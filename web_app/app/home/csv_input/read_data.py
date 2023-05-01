# Read in the tranhist file and return the data with analysised data
import csv
import re
import json
from .category import categoriesjson

def generateDict(bank, filename):
  if bank == "Starling":
    return generateDictStarling(filename)
  elif bank == "HSBC":
    return generateDictHSBC(filename)
  
#read in the csv file and return a dictionary storing the formatted data, a dictionary storing the months data 
# and a dictionary storing the summary of each month 
def generateDictHSBC(filename="./statement/TransHist.csv"):
  #read in the csv file
  with open(filename,encoding="utf-8-sig") as csvfile:
    allData = csv.reader(csvfile)
    #row[0]: date row[1]: detail of payment   row[2]:amount
    dates = []
    details = []
    amounts = []
    for row in allData:
      dates.append(row[0])
      details.append(row[1])
      amounts.append(row[2])

  dates.reverse()
  details.reverse()
  amounts.reverse()  
  #change details list into store list
  stores = []
  for row in details:
    spilted = re.split(r'\s{2,}', row)
    if len(spilted) == 3:
      stores.append(spilted[0])
    elif "************************************" in spilted[0]:
      stores.append(spilted[1])
    elif len(spilted) == 2:
      stores.append(spilted[0])
    elif "INT'L" in spilted[0]:
      stores.append(spilted[1])
    else:
      stores.append(row)

  #find the different month and the index of the first data of the month
  months = generateMonths(dates)

  data = generateData(months, dates, amounts, stores, "HSBC")

  return(data,months)

def generateDictStarling(filename="./statement/StarlingStatement.csv"):
  #read in the csv file
  with open(filename,encoding="utf-8-sig") as csvfile:
    allData = csv.reader(csvfile)
    dates = []
    stores = []
    amounts = []
    for row in allData:
      dates.append(row[0])
      stores.append(row[1])
      amounts.append(row[4])

  dates.reverse()
  stores.reverse()
  amounts.reverse()  

  months = generateMonths(dates)
  data = generateData(months, dates, amounts, stores, "Starling")
  return(data,months)

def generateData(months, dates, amounts, stores, bank):
  """
  store everything in dictionary
  """
  data = {}
  monthCount = 0
  amountDict = {}
  for (currentMonth,i) in months:
    data[currentMonth] = []
    #find the last index of this month
    try:
      (nextmonth,nextIndex) = months[monthCount+1]
    except:
      nextIndex = len(dates)

    for n in range(i, nextIndex):
      category = "Others"
      try:
        currentAmount = float(amounts[n])
      #handling the , in the amount
      except ValueError:
        amountList = amounts[n].split(',')
        realAmount = ""
        for a in amountList:
          realAmount+=a
        amounts[n]=realAmount

      #finding the categories of the data
      for categoryjson in categoriesjson:
        for item in categoriesjson[categoryjson]:
          if item.upper() in stores[n].upper():
            category = categoryjson

      #finding the paymeent method of the data      
      if "PAYPAL" in stores[n]:
        bank=f"Paypal({bank})"

      #store everything in the dict
      data[currentMonth].append({
        'Date': dates[n],
        'Month': currentMonth,
        'Store': stores[n],
        'Amount': amounts[n],
        'Category':category,
        'Bank':bank,
        'Excluded':False,
        'Notes':""
      })

    monthCount+=1
  return data

def generateMonths(dates):
  """
  Find the different month and the index of the first data of the month
  """
  splitDates = dates[0].split('/')
  initialMonth = splitDates[1]
  initialMonthYear = splitDates[2]
  months = [(f"{initialMonthYear}-{initialMonth}",0)] #list to store the months and the start index in list
  firstIndex=0
  nextMonth = initialMonth
  for day in dates:
    #reformat the date
    splitDay = day.split('/')
    dates[firstIndex] = splitDay[2]+"-"+splitDay[1]+"-"+splitDay[0]
    if splitDay[1] != nextMonth:
      nextMonth = splitDay[1]
      nextMonthYear = splitDay[2]
      months.append((f"{nextMonthYear}-{nextMonth}",firstIndex))
      firstIndex+=1
    else:
      firstIndex+=1
  return months

#output the data dictionary as separated csv files
def outputDataSeperateCsv(data,months):
  for (month,i) in months:
    filename1 = "./analysised/"+month.split('-')[0]+"_"+month.split('-')[1]+"_analysised.csv"
    with open(filename1, mode='w+', newline='') as csv_file:
        fieldnames = ['Date','Month', 'Store', 'Amount','Category','Bank','Excluded','Notes']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for item in data[month]:
          writer.writerow(item)
  print("outputted the data as seperated csv files")
  
#outout the data dictionary as one csv file
def outputDataOneCsv(data,months):
  with open("./analysised/all_analysised.csv", mode='w+', newline='') as csv_file:
    fieldnames = ['Date','Month', 'Store', 'Amount','Category','Bank','Excluded','Notes']
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
  