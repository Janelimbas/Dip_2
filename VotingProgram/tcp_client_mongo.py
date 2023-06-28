import socket
import json


class TCPclient():
    def __init__(self, sms):
        self.target_ip = 'localhost'
        self.target_port = 9997
        self.input_checking(sms)

    def client_runner(self):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))

        # client.send(self.client_sms)
        #
        #     received_from_server = client.recv(4096)
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
            self.register()
        else:
            print("Invalid Option")

    def get_all_data(self, sms):
        client = self.client_runner()
        sms = bytes(sms + ' ', "utf-8")
        client.send(sms)
        received_from_server = client.recv(4096)
        # print(received_from_server.decode("utf-8"))

        dict_data: dict = json.loads(received_from_server.decode("utf-8"))
        print(type(dict_data))
        print(dict_data)
        client.close()

    def register(self):
        print("\nThis is registration option ")
        # r_email = ''
        while True:
            r_email = input("Enter email for registration :")
            flag = self.email_checking(r_email)  # 1 or -1

            if flag == 1:
                break
            else:
                print("Email Form Invalid\nTry Again! ")

        print("Email From Valid ")

        try:
            option = input("Press 1 Registration for Voter:\nPress 2 Registration for Candidate!:")

            if option == '1':
                self.registration(r_email, option)
            elif option == '2':
                self.registration(r_email, option)

            else:
                print("Option not valid!")
                self.register()
        except Exception as err:
            print(err)

    def email_checking(self, r_email):
        name_counter = 0
        for i in range(len(r_email)):
            if r_email[i] == '@':
                # print("Name End Here")
                break
            name_counter += 1

        print("Name counter: ", name_counter)

        email_name = r_email[0:name_counter]
        email_form = r_email[name_counter:]

        # print(email_name)
        print(email_form)

        # checking for name
        name_flag = 0
        email_flag = 0
        for i in range(len(email_name)):
            aChar = email_name[i]
            if (ord(aChar) > 31 and ord(aChar) < 48) or (ord(aChar) > 57 and ord(aChar) < 65) or (
                    ord(aChar) > 90 and ord(aChar) < 97) or (ord(aChar) > 122 and ord(aChar) < 128):
                name_flag = -1
                break

        domain_form = ["@facebook.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com", "@apple.com", "@zoho.com",
                       "@gmail.com"]

        for i in range(len(domain_form)):

            if domain_form[i] == email_form:
                email_flag = 1
                break

        if name_flag == -1 or email_flag == 0:
            return -1

        else:
            return 1

    def registration(self, r_email, option):

        if self.email_check_inDB(r_email, option):
            try:
                pass1 = str(input(
                    "Enter your password to register:"))  # needs to code pw validation later, but here i cut off the space
                pass1 = pass1.replace(" ", "")
                pass2 = str(input("Enter your password again to register:"))
                pass2 = pass2.replace(" ", "")
                print(
                    "Don't worry about space in your pw. Currently we are removing all spaces in pw\nThis is your pw:",
                    pass1)

                if pass1 == pass2:

                    print("Passwords match!")
                    phone = int(input("Enter your phone number:"))
                    name = input("Enter your name to register:")
                    name = name.replace(" ", "")
                    print("You are {}".format(name))
                    user_info2: str = "candidate"
                    user_info1: str = "user"
                    point: int = 100
                    vote_point: int = 0

                    if option == '1':
                        try:
                            money = int(input("Enter your money to register:"))
                        except Exception as err:
                            print(err)
                        data_list = [name, r_email, pass1, phone, money, user_info1, point]
                    else:
                        client = self.client_runner()
                        sms = bytes("candidate_info", "utf-8")
                        client.send(sms)
                        info = client.recv(4096).decode("utf-8")
                        if info == '0':
                            i = 0
                        else:
                            candi_info = json.loads(info)
                            for i in candi_info:
                                i: int = int(i) + 1
                        index: int = i
                        candi_no: int = index + 1
                        data_list = [name, r_email, pass1, phone, user_info2, vote_point, candi_no]
                    self.final_registration(data_list, option)

                else:
                    print("Password not match:")
                    self.registration(r_email, option)


            except Exception as err:
                print(err)

        else:

            print("Your email was already register!")
            self.register()

    def email_check_inDB(self, email, option):

        client = self.client_runner()
        data = "emailcheck" + " " + email + " " + option

        client.send(bytes(data, "utf-8"))

        received = client.recv(4096).decode("utf-8")

        print(received)

        if received == "notExist":
            client.close()
            return True
        else:
            client.close()
            return False

    def final_registration(self, data_list, option):
        data_form = "register" + " " + data_list[0] + " " + data_list[1] + " " + data_list[2] + " " + str(
            data_list[3]) + " " + str(data_list[4]) + " " + str(data_list[5]) + " " + str(data_list[6]) + " " + str(
            option)

        client = self.client_runner()

        client.send(bytes(data_form, "utf-8"))

        recv = client.recv(4096).decode("utf-8")

        # print(recv)

        if recv:
            print("Registration Success!This is your id : ", recv)
            info = "login"
            self.login(info)

        client.close()

    def login(self, info):
        try:
            print("This is login Form")
            v_or_c = int(input("for voter or for candidate? \nEnter 1 for voter and 2 for candidate: "))
            l_email = input("Enter your email to login:")
            l_pass = str(input("Enter your password to login:"))
            l_pass = l_pass.replace(" ", "")

            client = self.client_runner()
            sms = info + ' ' + l_email + ' ' + l_pass + ' ' + str(v_or_c)  # login email password
            sms = bytes(sms, "utf-8")
            client.send(sms)
            received_from_server = client.recv(4096)
            received_from_server = received_from_server.decode('utf-8')
            length = len(received_from_server)
            if length == 33:
                print(received_from_server)
            else:
                user_info: dict = json.loads(received_from_server)
                self.option_choice(user_info, v_or_c)


        except Exception as err:
            print(err)

    def option_choice(self, user_info, who):
        print("Email :", user_info["email"])
        if who == 1:
            print("Money :", user_info["money"])
            print("Point :", user_info["point"])
        else:
            print("Info :", user_info["info"])
            print("Vote_point :", user_info["vote_point"])

        try:
            option = input("Press 1 to Get User Option:\nPress 2 To Get Main Option:\nPress 3 To Exit:")
            if option == '1':
                self.user_option(user_info, who)
            elif option == '2':
                self.input_checking("from_option")  # to write more option
            elif option == '3':
                exit(1)
            else:
                print("Invalid Option [X]")
                self.option_choice(user_info, who)

        except Exception as err:
            print(err)

    def user_option(self, user_info, who):
        if who == 1:
            try:
                option = int(input("Press 1 To Vote:\nPress 2 to get more points:\nPress 3 to Transfer Point:\n"
                                   "Press 4 To get Voting Ranking:\nPress 5 to change user information \n"
                                   "Press 6 to Delete Acc:\nPress 7 to exit:"))

                if option == 1:
                    self.voting(user_info)
                elif option == 2:
                    self.buy_points(user_info)
                elif option == 3:
                    self.transferPoint(user_info)

                else:
                    print("Invalid option")
                    self.user_option(user_info, who)

            except Exception as err:
                print(err)
                self.user_option(user_info, who)
        else:
            try:
                option = int(input("Press 1 To see Voters:\nPress 2 to see vote points:\nPress 3 to exit: "
                                   "to Exit:"))

                if option == 1:
                    print("These are people who voted u")
                elif option == 2:
                    print("You have this amount of vote")
                elif option == 3:
                    exit(1)

                else:
                    print("Invalid option")
                    self.user_option(user_info, who)

            except Exception as err:
                print(err)
                self.user_option(user_info, who)

    def voting_rules(self):
        print("100 kyats per point and 10 points per vote!\nWhen buying points, 10 points must be bought at least")

    def voting(self, user_info):
        client = self.client_runner()
        sms = bytes("candidate_info", "utf-8")
        client.send(sms)
        info = client.recv(4096)
        info = info.decode('utf-8')
        length = len(info)
        if length != 1:
            candi_info = json.loads(info)
        else:
            print("There is no candidate.")
            return
        # print(candi_info)
        # print(type(candi_info))
        for i in candi_info:  # 'int' object is not iterable ********error to fix for a 8
            # i: int = 0
            print("No:", int(i) + 1, "Name: ", candi_info[i]["name"], "vote_point", candi_info[i]["vote_point"])

        # must create another obj or it will cause errors
        client2 = self.client_runner()
        to_send = bytes("voter_info", "utf-8")
        client2.send(to_send)
        info = client2.recv(4096)
        info = json.loads(info.decode("utf-8"))
        for i in info:
            if info[i]["email"] == user_info["email"]:
                point = info[i]["point"]
                break

        try:
            print("vote system : 10 points per vote!")
            to_vote = int(input("Enter candidate no. u want to vote for: "))
            if to_vote > len(candi_info):
                print("Invalid option!")
                self.voting(user_info)
            else:
                want_vote = int(input("Enter the number of votes : "))
                cur_point = point
                can_vote = int(cur_point / 10)
                while can_vote <= 0:
                    print("You don't have enough points to vote.")
                    try:
                        choice = int(input(
                            "Press 1 to buy points: \n Press 2 to quit: \n Press 3 to read details about vote system: "))
                        if choice == 1:
                            self.buy_points(user_info)
                        elif choice == 2:
                            exit(1)
                        elif choice == 3:
                            self.voting_rules()
                            self.voting(user_info)
                        else:
                            print("Invalid option!")
                            self.voting(user_info)
                    except Exception as err:
                        print(err)

                if want_vote > can_vote >= 1:
                    if can_vote == 1:
                        print("You can vote for up to {} vote.".format(can_vote))
                    else:
                        print("You can vote for up to {} votes.".format(can_vote))
                    try:
                        option = int(input("Press 1 to buy points:\nPress 2 to continue voting:"))
                        if option == 1:
                            self.buy_points(user_info)
                        elif option == 2:
                            comfirm_vote = int(input("Enter the number of votes:"))
                            if comfirm_vote > can_vote:
                                print(
                                    "Please cast your vote within the allocated range based on the number of votes you currently possess.")
                                self.voting(user_info)
                            else:
                                to_send = "voting" + " " + user_info["email"] + " " + str(comfirm_vote) + " " + str(
                                    to_vote)
                                client = self.client_runner()
                                sms = bytes(to_send, "utf-8")
                                client.send(sms)
                                reply = client.recv(4096).decode("utf-8")
                                print(reply)
                                return
                        else:
                            print("Invalid option!")
                            self.voting(user_info)
                    except Exception as err:
                        print(err)


                elif can_vote >= want_vote:
                    if can_vote == 1:
                        print("You can vote for up to {} vote.".format(can_vote))
                    else:
                        print("You can vote for up to {} votes.".format(can_vote))
                    to_send = "voting" + " " + user_info["email"] + " " + str(want_vote) + " " + str(to_vote)
                    client = self.client_runner()
                    sms = bytes(to_send, "utf-8")
                    client.send(sms)
                    reply = client.recv(4096).decode("utf-8")
                    print(reply)
                    return

        except Exception as err:
            print(err)

        client.close()

    def buy_points(self, user_info):
        self.voting_rules()
        client2 = self.client_runner()
        to_send = bytes("voter_info", "utf-8")
        client2.send(to_send)
        info = client2.recv(4096)
        info = json.loads(info.decode("utf-8"))
        for i in info:
            if info[i]["email"] == user_info["email"]:
                money = info[i]["money"]
                break

        print("This is your money:", money)

        try:
            points_voters_want = int(input("Enter the amount of points u want to exchange : "))
            cur_money = int(money)
            can_ex_point = int(cur_money / 100)
            normal_price = can_ex_point * 100
            cost = int(points_voters_want * 100)
            if points_voters_want < 10:
                self.buy_points(user_info)
            else:
                while cost > cur_money:
                    print("You don't have enough money to buy points.")
                    choice = int(
                        input("Press 1 to add money:\nPress 2 to quit:\nPress 3 to go back to voting sector: "))
                    if choice == 1:
                        self.add_money(user_info)
                        return
                    elif choice == 2:
                        exit(1)
                    elif choice == 3:
                        self.voting(user_info)
                        return
                    else:
                        print("Invalid option!")
                        self.buy_points(user_info)
                    break

                print("You can exchange {} points for {} kyats.\n".format(can_ex_point, normal_price))
                to_send = "buy_points" + " " + user_info["email"] + " " + str(points_voters_want) + " " + str(cost)
                client = self.client_runner()
                sms = bytes(to_send, "utf-8")
                client.send(sms)
                reply = client.recv(4096).decode("utf-8")
                print(reply)
                self.user_option(user_info,1)
                return

        except Exception as err:
            print(err)

    def add_money(self, user_info):
        try:
            print("The amount must be at least 100 kyats to add.")
            money_toAdd = int(input("Enter the amount of money u want to add : "))
            if money_toAdd < 100:
                self.add_money(user_info)
            else:
                to_send = "add_money" + " " + user_info["email"] + " " + str(money_toAdd)
                client1 = self.client_runner()
                sms = bytes(to_send, "utf-8")
                client1.send(sms)
                reply = client1.recv(4096).decode("utf-8")
                print(reply)
                self.buy_points(user_info)
                return

        except Exception as err:
            print(err)

    def transferPoint(self, user_info):
        client = self.client_runner()
        sms = bytes("voter_info", "utf-8")
        client.send(sms)
        info = client.recv(4096)
        info = info.decode('utf-8')
        voter_info = json.loads(info)

        try:
            amount = int(input("Enter the amount of points u want to transfer:"))
            for i in voter_info:
                if voter_info[i]["email"] == user_info["email"]:
                    if voter_info[i]["point"] < 1:
                        print("You don't have any point.")
                        self.buy_points(user_info)
                    elif voter_info[i]["point"] < amount:
                        print("This is your point : {}".format(voter_info[i]["point"]))
                        print("You don't have enough point.Please transfer in the range of what u have.")
                        self.transferPoint(user_info)
                    else:
                        receiver = input("Enter receiver's email:")
                        client1 = self.client_runner()
                        sms = 'transfer' + ' ' + user_info["email"] + ' ' + receiver + ' ' + str(amount)
                        sms = bytes(sms, "utf-8")
                        client1.send(sms)
                        received_from_server = client1.recv(4096)
                        received_from_server = received_from_server.decode('utf-8')
                        print(received_from_server)
                        self.user_option(user_info, 1)
        except Exception as err:
            print(err)


if __name__ == "__main__":
    while True:
        sms = input("Enter some data to send:")
        tcp_client = TCPclient(sms)
