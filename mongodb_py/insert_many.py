import pymongo

import random
connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2_test"]
collection = database["user_info"]

if __name__ == '__main__':


    for i in range(10):
        user_id = random.randint(10, 10000)
        name: str = "win"+str(i)
        email: str = "win"+str(i)+"@gmail.com"
        password: str = "12345"
        phone: int = 94537
        point: int = 100

        info:str = "User info - name : "+str(name)+" , id : "+str(user_id)

        data_form = {"_id": user_id,"name":name,"email": email, "password": password, "phone": phone,"info":info,"point":point}

        ids = collection.insert_one(data_form)
        print("inserted id :", ids.inserted_id)