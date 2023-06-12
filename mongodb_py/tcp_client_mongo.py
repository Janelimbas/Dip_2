import socket
import json


class TCPclient():
    def __init__(self, sms):
        self.target_ip = 'localhost'
        self.target_port = 9998
        self.input_checking(sms)

    def client_runner(self):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))

        # client.send(self.client_sms)
        #
        #     received_from_server = client.recv(1024)
        #
        #     recv_sms = received_from_server.decode("utf-8")
        #
        #     print("$:", recv_sms)
        #
        #     client.close()
        return client  # to send and received data

    def input_checking(self, sms):
        if sms == "gad":
            self.get_all_data(sms)

        elif sms == "login":
            self.login(sms)

        elif sms == "reg":
            self.register(sms)
        else:
            print("Invalid Option")

    def get_all_data(self, sms):
        client = self.client_runner()
        sms = bytes(sms + ' ', "utf-8")
        client.send(sms)
        received_from_server = client.recv(1024)
        # print(received_from_server.decode("utf-8"))

        dict_data: dict = json.loads(received_from_server.decode("utf-8"))
        print(type(dict_data))
        print(dict_data)
        client.close()

    def login(self, info):
        try:
            print("This is login Form")
            l_email = input("Enter your email to login:")
            l_pass = input("Enter your password to login:")

            client = self.client_runner()
            sms = info + ' ' + l_email + ' ' + l_pass  # login email pw
            sms = bytes(sms, 'utf-8')
            client.send(sms)
            received_from_server = client.recv(1024)
            recv_from_server = received_from_server.decode('utf-8')
            length = len(recv_from_server)
            if length == 33:
                print(recv_from_server)
            else:
                user_info: dict = json.loads(recv_from_server)
                self.option_choice(user_info, client)


        except Exception as err:
            print(err)

    def option_choice(self, user_info, client):
        print("Email :", user_info["email"])
        print("Info :", user_info["info"])
        print("Point :", user_info["point"])

        try:
            option = input("Press 1 to Get User Option:\nPress 2 To Get Main Option:\nPress 3 To Exit:")
            if option == '1':
                self.user_option(user_info, client)
            elif option == '2':
                self.input_checking("from_option")  # to write more option
            elif option == '3':
                exit(1)
            else:
                print("Invalid Option [X]")
                self.option_choice(user_info, client)

        except Exception as err:
            print(err)

    def user_option(self, user_info, client):
        try:
            option = input("Press 1 To Vote:\nPress 2 to get more points:\nPress 3 to Transfer Point:\n"
                           "Press 4 To get Voting Ranking:\nPress 5 to change user information \nPress 6 to Delete Acc:\nPress 7 "
                           "to Exit:")

            if option == '1':
                self.voting(user_info)

            else:
                print("Invalid option")
                self.user_option(user_info, client)

        except Exception as err:
            print(err)
            self.user_option(user_info, client)

    def voting(self, user_info):
        client = self.client_runner()
        sms = bytes("candidate_info", "utf-8")
        client.send(sms)

        info = client.recv(1024)
        candi_info = json.loads(info.decode("utf-8"))
        print(candi_info)
        # print(type(candi_info))
        for i in candi_info:
            print("No:",i," Name:",candi_info[i]["name"]," Point",candi_info[i]["vote_point"])

        client.close()

    def register(self, info):
        try:
            print("This is registration option ")
            r_email = str(input("Enter your email to register:"))
            client = self.client_runner()
            sms = info + ' ' + r_email  # reg email password
            sms = bytes(sms, "utf-8")
            client.send(sms)

            received_from_server = client.recv(1024)
            reply = received_from_server.decode("utf-8")
            length = len(reply)

            if length == 56:
                print(reply)
                self.register(info)
            else:
                to_ask_name = str(input(reply))
                r_name = bytes(to_ask_name, 'utf8')
                client.send(r_name)

                to_ask_pass = client.recv(1024)
                r_pass = input(to_ask_pass.decode("utf-8"))
                client.send(bytes(r_pass, 'utf-8'))

                to_ask_ph = client.recv(1024)
                r_phone = input(to_ask_ph.decode("utf-8"))
                client.send(bytes(r_phone, 'utf-8'))

                #to get user data
                user_data_from_server = client.recv(1024)
                user_info: dict = json.loads(user_data_from_server.decode('utf-8'))
                print(user_info)


        except Exception as err:
            print(err)


if __name__ == "__main__":
    while True:
        sms = input("Enter some data to send:")
        tcp_client = TCPclient(sms)

