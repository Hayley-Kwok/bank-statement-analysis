#Storing all categories in a dictionary
import json

categoriesjson = {"Grocery":["TESCO","ICELAND","POUNDLAND","CO-OP","HOLLAND & BARRETT","POLISH GROCERY LTD","YI-MART","MORRISON","SAINSBURYS","VILLAGE STORE","MARKS&SPENCER","HOLLANDBAR","WILKO","B&M","TJ HUGHES","SAVERS HEALTH","SAINSBURY'S"],
"Fashion":["NEW LOOK","PRIMARK","HOLLISTER","Lovisa","ASOSCOMLTD","FASHIONRET","Deichmann","UNIQLO","ACCESSORIZE","CATH KIDSTON","SKINNYDIP","HMHENNESMA","H AND M","H & M","J D SPORTS"],
"Cosmetic":["BOOTS","CULT BEAUT","LOOKFANTAS","SUPERDRUGS","THE BODY SHOP","SUPERDRUG","HQHAIR","DECIEM","BODYSHOP","HQ HAIR","BODYCARE","BEAUTYBAYC"],
#WATERWOR -> Weatherspoon, AMRC cafe -> diamond UPTON GROUP LIMITE-> vending machines
"Eatout":["WETHERSPOO","DELIVEROO","DOMINOS","MCDONALDS","FIVE GUYS","REVOLUCION - DE CU","FIREPIT","Just Eat","WATERWOR","ITSU","HAUTECATERS","NANDOS","TACO BELL","SUBWAY","AMRC CAFE","CAVENDISH","STS SU LEVEL 3 CAF","LET US SUSHI","UPTON GROUP LIMITE",
          "OISOI","KRISPY KREME","DIAMOND CAFE","DASHU","MR PRETZELS","WAGAMAMA","THE CABIN PANCAKE","PAUL UK","VENCHI","LADUREE","CRUSSH","BURGER & LOBSTER","PASTY SHOP","BURGER KING","CAFFE NERO","COMMONS CAFE","KFC","ZIZZI","GBK","AUNTIE ANNES",
          "CORPORATION","LITTLE SNACK BAR","Sushi Express","TSUKI","BARBURRITO","ZINC","PP*DOUGHNOTTS"],
"Transport":["TRAINLINE","FIRST BUS","Uber","First South","STGCOACH","TFL TRAVEL"],
"Necessities":["CIRCUITLAU","H3G","H*G"],
"Non-necessities":["AMZNM","Amazon","AMZ","DISNEY","Cinema","PYRAMID POSTERS LI","T K MAXX","Google Pla","CINEMA","IKEA","VUE","WH SMITH","VANS","FORBIDDEN PLANET","DEBENHAMS"]}

#output the dictionary as a json file
def outputCategoryJson(data,filename='categories.json'):
  with open(filename, 'w+') as outfile:
    json.dump(data, outfile)
  print("Finished Outputting the categories dictionary to "+filename)

if __name__ == "__main__":
  outputCategoryJson(categoriesjson)
  # print(categoriesDict)


