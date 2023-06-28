import socket
import json

import pymongo

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
col = database["user_info"]
candi = database["candidate"]

class TCPserver():
    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9997
        self.toSave = {}

    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen()
        print("Server listen on port:{} and ip {}".format(self.server_port, self.server_ip))
        try:
            while True:
                client, address = server.accept()
                print("Accepted Connection from - {} : {} ".format(address[0], address[1]))
                self.handle_client(client)
                client.close()
        except Exception as err:
            print(err)

    def handle_client(self, client_socket):
        data_list = []
        with client_socket as sock:
            from_client = sock.recv(1024)
            data_list = from_client.decode("utf-8").split(' ')  # login email password

            # data_list = ["login","email","password"]

            #     output = subprocess.getoutput("dir")
            #     # result = output.stdout.decode()
            #
            #     # return_valued = os.system(received_data)

            if data_list[0] == "gad":
                print("received command :", data_list[0])
                self.get_all_data(sock)

            elif data_list[0] == "login":
                self.login_checking(sock, data_list)

            elif data_list[0] == "candidate_info":
                self.candidate_info(sock)

            elif data_list[0] == "voter_info":
                self.user_info(sock)

            elif data_list[0] == "emailcheck":

                self.email_checking(data_list[1], data_list[2], sock)

            elif data_list[0] == "register":

                self.registration(data_list, sock)

            elif data_list[0] == "voting":
                self.voting(sock,data_list)

            elif data_list[0] == "buy_points":
                self.buy_points(sock,data_list)

            elif data_list[0] == "add_money":
                self.add_money(sock,data_list)

            elif data_list[0] == "transfer":
                self.transferPoint(sock,data_list)

            else:
                sms = bytes("Invalid Option", "utf-8")
                sock.send(sms)

    def get_all_data(self, sock):
        data: dict = {}
        id = 0
        for i in col.find({}, {"_id": 0, "email": 1, "password": 1}):
            id = len(data)
            dataform = {"email": i["email"], "password": i["password"]}
            data.update({id: dataform})
        print(data)
        str_data = json.dumps(data)

        str_data = bytes(str_data, 'utf-8')
        sock.send(str_data)

    def login_checking(self, sock, data_list):
        l_email = data_list[1]
        l_password = data_list[2]
        flag = -1
        sms = {}
        if data_list[3] == '1':
            for i in col.find({}, {"_id": 0, "email": 1, "password": 1, "money": 1, "info": 1, "point": 1}):
                if i["email"] == l_email and i["password"] == l_password:
                    flag = 1
                    sms = {"email": i["email"], "money": i["money"], "point": i["point"]}
                    sms = json.dumps(sms)

                    break
        else:
            for i in candi.find({}, {"_id": 0, "email": 1, "password": 1, "info": 1, "vote_point": 1}):
                if i["email"] == l_email and i["password"] == l_password:
                    flag = 1
                    sms = {"email": i["email"], "info": i["info"], "vote_point": i["vote_point"]}
                    sms = json.dumps(sms)

                    break

        if flag == 1:
            str_data = bytes(sms, 'utf-8')
            sock.send(str_data)
        else:
            str_data = bytes("User name and password not found!", 'utf-8')
            sock.send(str_data)

    def candidate_info(self, sock):

        try:
            to_send:dict = {}
            candi_count = candi.count_documents({})  # Count the number of documents in the collection

            if candi_count > 0:
                for i in candi.find({}, {"_id": 0, "name": 1, "vote_point": 1}):
                    id = len(to_send)
                    to_update = {id: {"name": i["name"], "vote_point": i["vote_point"]}}
                    to_send.update(to_update)
                    to_reply = json.dumps(to_send)
            else:
                to_reply = "0"

            sock.send(bytes(to_reply, "utf-8"))

        except Exception as err:
            print("candiate db access err.", err)
            sock.send(bytes("candi_db_error", "utf-8"))

    def user_info(self, sock):

        try:
            to_send = {}
            for i in col.find({}, {"_id": 0,"name" : 1 , "email": 1, "point": 1,"money":1}):
                # print(i["name"], i["point"])
                id = len(to_send) + 1
                to_update = {id: {"name" : i["name"],"email": i["email"], "point": i["point"],"money": i["money"]}}
                to_send.update(to_update)

            to_send = json.dumps(to_send)

            sock.send(bytes(to_send, "utf-8"))
        except Exception as err:
            print("user db access err:", err)
            sock.send(bytes("user_db_error", "utf-8"))

    def email_checking(self, email, who, sock):
        email_exist = 0
        if who == '1':
            for i in col.find({}, {"_id": 0, "email": 1}):
                if i["email"] == email:
                    email_exist = 1
        else:
            for i in candi.find({}, {"_id": 0, "email": 1}):
                if i["email"] == email:
                    email_exist = 1

        if email_exist == 0:  # email not already exist
            sock.send(bytes("notExist", "utf-8"))

        else:
            sock.send(bytes("exist", "utf-8"))

    def registration(self, data_list: list, sock):
        if data_list[8] == '1':
            data_form = {"name":data_list[1], "email": data_list[2], "password": data_list[3], "phone": int(data_list[4]), "money": data_list[5],
                         "info": str(data_list[6]),"point": int(data_list[7])}
            ids = col.insert_one(data_form)
        else:
            data_form = {"name": data_list[1], "email": data_list[2], "password": data_list[3],
                         "phone": int(data_list[4]), "info": str(data_list[5]),
                         "vote_point": int(data_list[6]), "candi_no": data_list[7]}
            ids = candi.insert_one(data_form)

        print("Registration success for :", ids.inserted_id)

        sock.send(bytes(str(ids.inserted_id), "utf-8"))

    def voting(self,sock,data_list):
        for i in col.find({}, {"_id": 0, "email": 1,"name": 1, "point": 1}):
            if data_list[1] == i["email"]:
                after_vote_pt = i["point"]-(int(data_list[2])*10)
                # Update the document
                filter_query = {'email': i["email"]}  # Filter for the document to update, better to use sth unique for each document
                update_query = {'$set': {'point': after_vote_pt}}  # Update the 'point' field to data in there

                # Perform the update
                col.update_one(filter_query, update_query)
                break

        for i in candi.find({}, {"_id": 0,"candi_no":1, "email": 1,"name": 1, "vote_point": 1}):
            if data_list[3] == i["candi_no"]:
                after_vote_vpt = i["vote_point"]+ int(data_list[2])

                filter_query = {'candi_no': i["candi_no"]}
                update_query = {'$set': {'vote_point': after_vote_vpt}}
                candi.update_one(filter_query, update_query)
                to_send = str("Currently you voted {} votes for candidate {}.".format(data_list[2],data_list[3]))
                sock.send(bytes(to_send, "utf-8"))
                break

    def buy_points(self, sock,data_list):
        for i in col.find({}, {"_id": 0, "email": 1, "point": 1, "money":1}):
            if data_list[1] == i["email"]:
                after_buy_pt = i["point"]+int(data_list[2])
                after_buy_money = int(i["money"])-int(data_list[3])
                filter_query = {'point': i["point"],'money': i["money"]}
                update_query = {'$set': {'point': after_buy_pt, 'money':after_buy_money}}
                col.update_one(filter_query, update_query)
                to_send = str("Purchase succeeds! You bought {} points with {} kyats.".format(data_list[2], data_list[3]))
                sock.send(bytes(to_send, "utf-8"))
                break

    def add_money(self, sock,data_list):
        for i in col.find({}, {"_id": 0, "email": 1, "money":1}):
            if data_list[1] == i["email"]:
                after_adding_money = int(i["money"])+int(data_list[2])
                filter_query = {'email': i["email"]}
                update_query = {'$set': {'money':after_adding_money}}
                col.update_one(filter_query, update_query)
                to_send = str("This is your updated balance: {} kyats.".format(after_adding_money))
                sock.send(bytes(to_send, "utf-8"))

    def transferPoint(self,sock,data_list):
        if data_list[1] != data_list[2]:
            email_found = -1
            for i in col.find({},{"_id":0,"email":1,"point":1}):
                if data_list[2] == i["email"]:
                    email_found = 1;
                    after_getting_point = i["point"]+int(data_list[3])
                    filter_query = {'email': i["email"]}
                    update_query = {'$set': {'point':after_getting_point}}
                    col.update_one(filter_query, update_query)
                    to_send = str("You transfer {} points to {}.".format(data_list[3],data_list[2]))
                    sock.send(bytes(to_send, "utf-8"))

            if email_found == -1:
                to_send = str("Receiver email doesn't exist.")
                sock.send(bytes(to_send, "utf-8"))
            else:
                for i in col.find({},{"_id":0,"email":1,"point":1}):
                        if data_list[1] == i["email"]:
                            after_sending_point = i["point"] - int(data_list[3])
                            filter_query = {'email': i["email"]}
                            update_query = {'$set': {'point': after_sending_point}}
                            col.update_one(filter_query, update_query)

        else:
            to_send = str("You cannot transfer yourself.")
            sock.send(bytes(to_send, "utf-8"))


if __name__ == '__main__':
    tcpserver = TCPserver()
    tcpserver.main()
