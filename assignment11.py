#bank with linked list and use mongodb only for saving data
#login, register, transfer money
#data, uname, email, pw, amount, ph

import pymongo

connection = pymongo.MongoClient("localhost", 27017)
database = connection["user_database"]
users_collection = database["user_info"]
class Node:
    def __init__(self, user_data):
        self.user_data = user_data
        self.next_node = None

class LinkedList:
    def __init__(self):
        self.head = None

    def LinkedListEmpty(self):
        self.user_count = users_collection.count_documents({})  # Count the number of documents in the collection

        if self.user_count > 0:
            head_node = None  # Initialize the head node to None
            current_node = None  # Initialize the current node to None
            id = 1

            for i in users_collection.find({},
                                           {"_id": 0, "name": 1, "email": 1, "phone": 1, "money": 1, "password": 1}):
                node_data = {id:{"name": i["name"], "email": i["email"], "phone": i["phone"], "money": i["money"],
                             "password": i["password"]}}
                id+= 1
                new_node = Node(node_data)

                if head_node is None:
                    head_node = new_node
                    current_node = new_node
                else:
                    current_node.next_node = new_node
                    current_node = new_node

            return head_node
        else:
            return None

    def insertNode(self, user_data):
        new_node = Node(user_data)
        if self.head == None:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next_node is not None:
                current_node = current_node.next_node
            current_node.next_node = new_node

    def email_format_checking(self,r_email):
        name_counter = 0
        for i in range(len(r_email)):
            if r_email[i] == '@':
                # print("Name End Here")
                break
            name_counter += 1

        email_name = r_email[0:name_counter]
        email_form = r_email[name_counter:]

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

    def pw_check(self,email):
        current = LinkedList.LinkedListEmpty()
        while current is not None:
            user_data = current.user_data
            for key in user_data:
                if user_data[key]['email'] == email:
                    return user_data[key]['password']
            current = current.next_node
        return None

    def get_money_by_email(self, email):
        current = LinkedList.LinkedListEmpty()
        while current is not None:
            user_data = current.user_data
            for key in user_data:
                if user_data[key]['email'] == email:
                    return user_data[key]['money']
            current = current.next_node
        return False

    def update_money_by_email(self, email, amount:int,who):
        current = LinkedList.LinkedListEmpty()
        while current is not None:
            user_data = current.user_data
            for key in user_data:
                if user_data[key]['email'] == email:
                    if who == 1:
                        # user_data[key]['money'] += amount
                        self.update_money(email,amount,1)
                    else:
                        # user_data[key]['money'] -= amount
                        self.update_money(email,amount,2)


            current = current.next_node
        return False  # Email not found
    def email_exist_check(self, email):
        current = LinkedList.LinkedListEmpty()
        while current is not None:
            user_data = current.user_data
            for key in user_data:
                if user_data[key]['email'] == email:
                    return True  # Email found
            current = current.next_node
        return False  # Email not found

    def phone_exist_check(self,phone):
        current = LinkedList.LinkedListEmpty()
        while current is not None:
            user_data = current.user_data
            for key in user_data:
                if user_data[key]['phone'] == phone:
                    return True  # ph found
            current = current.next_node
        return False  # ph not found

    def update_money(self,email,money,who):
        for i in users_collection.find({}, {"_id": 0, "email": 1, "money":1}):
            if i['email'] == email:
                if who == 1:
                    after_updating_money = int(i["money"])+int(money)
                else:
                    after_updating_money = int(i["money"])-int(money)
                filter_query = {'email': i["email"]}
                update_query = {'$set': {'money':after_updating_money}}
                users_collection.update_one(filter_query, update_query)



LinkedList = LinkedList()


# User registration
def register_user():
    ph = 0
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    if LinkedList.email_format_checking(email)!= 1:
        print("Email format is not valid!")
        register_user()
    else:
        if LinkedList.email_exist_check(email) is True:
            print("Email is already registered!")
            register_user()
        else:
            try:
                ph = int(input("Enter your phone number: ")) #leave ph format checking
            except Exception as err:
                print(err)
                register_user()
            if LinkedList.phone_exist_check(ph) is True:
                print("Phone number is already registered!")
                register_user()
            try:
                money = int(input("Enter your money: ")) #leave money input checking
            except Exception as err:
                print(err)
                register_user()
            password = input("Enter your password: ") #leave strong pw checking

            user_data = {
                "name": name,
                "email": email,
                "phone": ph,
                "money":money,
                "password": password
            }
            LinkedList.insertNode(user_data)
            users_collection.insert_one(user_data)

            # LinkedList.append(user_data)
            print("Registration successful!")


# User login
def login_user():
    current = LinkedList.LinkedListEmpty()
    if current is not None:
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        lemail = LinkedList.email_exist_check(email)
        if lemail is True:
            lpw = LinkedList.pw_check(email)
            if password == lpw:
                print("Login successful!")
                print("Press 1 to transfer money:\nPress 2 to exit: ")
                option = input("Enter your option: ")
                if option == "1":
                    transfer_money(email)
                elif option == "2":
                    exit(0)
                else:
                    print("Invalid option!")
            else:
                print("Invalid credentials!")
        else:
            print("Invalid credentials!")
    else:
        print("Nothing in the db.")

def transfer_money(email): #transfer money using email
    receiver_email = input("Please enter receiver's email: ")
    current_money = LinkedList.get_money_by_email(email)
    if LinkedList.email_exist_check(receiver_email) is False:
        print("Email is not existed!")
    else:
        try:
            amount = int(input("Please enter the amount to transfer: "))
        except Exception as err:
            print(err)
            transfer_money()
        if amount>int(current_money):
            print("Insufficient balance!\nThis is your money:",current_money)
            login_user()
        else:
            LinkedList.update_money_by_email(email,amount,2)
            LinkedList.update_money_by_email(receiver_email,amount,1)
            print("Transfer successfully! This is your current amount: ",current_money-amount)


# Main program
while True:
    print("Press 1 to Register:\nPress 2 to Login:\nPress 3 to exist:")
    choice = input("Enter your choice: ")

    if choice == "1":
        register_user()
    elif choice == "2":
        login_user()
    elif choice == "3":
        exit(0)
    else:
        print("Invalid choice. Please try again.")