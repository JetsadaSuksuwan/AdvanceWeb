import pymongo

myclient = pymongo.MongoClient("mongodb://admin:QCEhtg52239@node9141-advweb-03.app.ruk-com.cloud:11157")
mydb = myclient["MongoDB"]
mycol = mydb["Game"]

for x in mycol.find():
  print(x)