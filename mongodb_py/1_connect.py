#not includeed in assignment, this is just for practice

import pymongo #to connect py and mongodb

import random

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
collection = database["user_info"]

# data = {"name":"kitty","email":"dkf1@gmail.com"}
# ids=collection.insert_one(data)
# print("ids",ids.inserted_id)

if __name__ == '__main__':
    while True:
        try:
            user_id = random.randint(10, 10000)
            email: str = input("Enter useremail:")
            password: str = input("Enter user password:")
            phone: int = int(input("Enter user phone:"))

            data_form = {"_id": user_id, "email": email, "password": password, "phone": phone}

            ids = collection.insert_one(data_form) #return id
            print("inserted id :", ids.inserted_id)
        except Exception as err:
            print(err)
