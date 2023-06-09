import socket

import json

import pymongo
import random

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2_test"]
col = database["user_info"]

candi = database["candidate"]


class TCPserver():
    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9998
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

            elif data_list[0] == "reg":
                self.registration(sock, data_list)
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
        for i in col.find({}, {"_id": 0, "email": 1, "password": 1, "info": 1, "point": 1}):
            if i["email"] == l_email and i["password"] == l_password:
                flag = 1
                sms = {"email": i["email"], "info": i["info"], "point": i["point"]}
                sms = json.dumps(sms)
                # to_send = bytes(sms, "utf-8")
                # sock.send(to_send)
                # break

        if flag == 1:
            str_data = bytes(sms, 'utf-8')
            sock.send(str_data)
        else:
            str_data = bytes("User name and password not found!", 'utf-8')
            sock.send(str_data)

    def candidate_info(self, sock):

        try:
            to_send = {}
            for i in candi.find({}, {"_id": 0, "name": 1, "vote_point": 1}):
                print(i["name"], i["vote_point"])
                id = len(to_send) + 1
                to_update = {id: {"name": i["name"], "vote_point": i["vote_point"]}}
                to_send.update(to_update)

            to_send = json.dumps(to_send)

            sock.send(bytes(to_send, "utf-8"))
        except Exception as err:
            print("candiate db access err:", err)

            sock.send(bytes("candi_db_error", "utf-8"))

    def registration(self, sock, data_list):
        r_email = data_list[1]
        email_exists = False
        for i in col.find({}, {"_id": 0, "email": 1}):
            if i["email"] == r_email:
                email_exists = True
                to_send = bytes("Email already registered! Please try with another email!","utf-8")
                sock.send(to_send)
                break

        if email_exists == False:

            id = random.randint(10, 10000)

            to_ask_name = bytes("Enter your name to register:", "utf-8")
            sock.send(to_ask_name)
            getting_name = sock.recv(1024)
            name = getting_name.decode("utf-8")

            to_ask_pass = bytes("Enter your password to register:","utf-8")
            sock.send(to_ask_pass)
            getting_pw = sock.recv(1024)
            r_pass = getting_pw.decode("utf-8")

            to_ask_ph = bytes("Enter your phone number to register:", "utf-8")
            sock.send(to_ask_ph)
            getting_ph = sock.recv(1024)
            r_phone = getting_ph.decode("utf-8")

            point:int = 100
            info: str = "User info - name: " + str(name) + ", id : " + str(id)

            data_form = {"_id":id,"name":name, "email":r_email, "password":r_pass,"phone": r_phone,"info":info, "point": point}
            # to update data to mongodb
            col.insert_one(data_form)

            #to send user's data to user
            to_send = json.dumps(data_form)
            user_data = bytes(to_send,"utf-8")
            sock.send(user_data)


if __name__ == '__main__':
    tcpserver = TCPserver()
    tcpserver.main()