#not includeed in assignment, this is just for practice

import pymongo

connection = pymongo.MongoClient("localhost",27017)
database = connection["ncc_dip2"]
collection = database["user_info"]
r_email = input("Enter ur email to register : ")

for i in collection.find({},{"_id":0, "email":1}): #finding specific data on db
    # print(i)
    # print(i["email"])
    if r_email == i["email"]:
        print("Already registered!")
        break