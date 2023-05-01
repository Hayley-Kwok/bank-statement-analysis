#Storing all categories in a dictionary
import json

categoriesjson = {"Grocery":["TESCO","ICELAND","CO-OP","HOLLAND & BARRETT","POLISH GROCERY LTD","YI-MART","MORRISON","SAINSBURYS","VILLAGE STORE","MARKS&SPENCER","HOLLANDBAR","B&M","TJ HUGHES","SAVERS HEALTH","SAINSBURY'S","SAMY LTD","ALDI","WAITROSE", "KH ORIENTAL GROUP", "SAMY LIMITED 31106", "Kh Oriental", "Hang Sing Hong"],
"Fashion":["NEW LOOK","PRIMARK","HOLLISTER","Lovisa","ASOSCOMLTD","FASHIONRET","Deichmann","UNIQLO","ACCESSORIZE","CATH KIDSTON","SKINNYDIP","HMHENNESMA","H AND M","H & M","J D SPORTS", "BOOHOO", "PAYPAL *MISSGUIDED", "WWW.MISSGUIDED.CO.", "HM.COM"],
"Cosmetic":["BOOTS","CULT BEAUT","LOOKFANTAS","SUPERDRUGS","THE BODY SHOP","SUPERDRUG","HQHAIR","DECIEM","BODYSHOP","HQ HAIR","BODYCARE","BEAUTYBAYC"],
#WATERWOR -> Weatherspoon, AMRC cafe -> diamond UPTON GROUP LIMITE-> vending machines
"Eatout":["WETHERSPOO","DELIVEROO","DOMINOS","MCDONALDS","FIVE GUYS","REVOLUCION - DE CU","FIREPIT","Just Eat","WATERWOR","ITSU","HAUTECATERS","NANDOS","TACO BELL","SUBWAY","AMRC CAFE","CAVENDISH","STS SU LEVEL 3 CAF","LET US SUSHI","UPTON GROUP LIMITE",
          "OISOI","KRISPY KREME","DIAMOND CAFE","DASHU","MR PRETZELS","WAGAMAMA","THE CABIN PANCAKE","PAUL UK","VENCHI","LADUREE","CRUSSH","BURGER & LOBSTER","PASTY SHOP","BURGER KING","CAFFE NERO","COMMONS CAFE","KFC","ZIZZI","GBK","AUNTIE ANNES",
          "CORPORATION","LITTLE SNACK BAR","Sushi Express","TSUKI","BARBURRITO","ZINC","PP*DOUGHNOTTS", "GREGGS PLC", "HUNGRYPANDA.CO", "DOMINO S PIZZA", "OHM SHEFFIELD", "LETS SUSHI", "Greggs", "Cuppacha"],
"Transport":["TRAINLINE","FIRST BUS","Uber","First South","STGCOACH","TFL TRAVEL"],
"Bills":["CIRCUITLAU","H3G","H*G", "NPOWER", "YORKSHIRE WATER", "AMAZON PRIME*6G42I", "GOOGLE *YouTube Mu", "GOOGLE *YouTubePre", "giffgaff", "E.ON NEXT", "Nya*huttons Buildings"],
"Non-necessities":["AMZNM","Amazon","AMZ","DISNEY","Cinema","PYRAMID POSTERS LI","T K MAXX","Google Pla","CINEMA","IKEA","VUE","WH SMITH","VANS","FORBIDDEN PLANET","DEBENHAMS"],
"Home Stuff":["POUNDLAND","WILKO"],
"Salary":["CERTARA UK LIMITED"],
"Games": ["Nintendo Of Europe Gmb Frankfurt Am Deu", "Humblebundle", "Steam"]}

#output the dictionary as a json file
def outputCategoryJson(data,filename='categories.json'):
  with open(filename, 'w+') as outfile:
    json.dump(data, outfile)
  print("Finished Outputting the categories dictionary to "+filename)

if __name__ == "__main__":
  outputCategoryJson(categoriesjson)
  # print(categoriesDict)


