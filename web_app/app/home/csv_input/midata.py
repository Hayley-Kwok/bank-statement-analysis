#for hsbc
# Changing the midata file to the tranhist format
import csv
import re

# change the file into the tranhist format and return the data as a list
def getData(filename="./statement/midata.csv"):
  #read in the csv file
  with open(filename,encoding="utf-8-sig") as csvfile:
    allData = csv.reader(csvfile)
    #row[0]: date row[1]: detail of payment   row[2]:amount
    dates = []
    details = []
    amounts = []
    for row in allData:
      dates.append(row[0])
      details.append(row[2]+"       "+row[1])
      amounts.append(row[3].replace("£",""))

    data = []  
    for (i,date) in enumerate(dates):
      data.append([date,details[i],amounts[i]])

  return(data)

# output the data as a csv file
def outputCsv(data):
  with open("./statement/midata_tranhist.csv", mode='w+', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for d in data:
      writer.writerow(d)

if __name__ == "__main__":
  data = getData()
  print(data)
  outputCsv(data)

