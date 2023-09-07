# to fix update option

class Node:
    def __init__(self, name, email, password, phone_number):
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, name, email, password, phone_number):
        self.root = self.insert_recursive(self.root, name, email, password, phone_number)

    def insert_recursive(self, current, name, email, password, phone_number):
        if current is None:
            return Node(name, email, password, phone_number)

        if phone_number < current.phone_number:
            current.left = self.insert_recursive(current.left, name, email, password, phone_number)
        elif phone_number > current.phone_number:
            current.right = self.insert_recursive(current.right, name, email, password, phone_number)

        return current

    def is_email_unique(self, email):
        return self.check_email_recursive(self.root, email)

    def check_email_recursive(self, root, email):
        if root is None:
            return True
        if email == root.email:
            return False
        if email < root.email:
            return self.check_email_recursive(root.left, email)
        return self.check_email_recursive(root.right, email)

    def is_phone_unique(self, phone):
        return self.check_phone_recursive(self.root, phone)

    def check_phone_recursive(self, root, phone):
        if root is None:
            return True
        if phone == root.phone_number:
            return False
        if phone < root.phone_number:
            return self.check_phone_recursive(root.left, phone)
        return self.check_phone_recursive(root.right, phone)

    def search(self, value):
        return self.search_recursive(self.root, value)

    def search_recursive(self, current, value):
        if current is None:
            return None

        if value == str(current.phone_number) or value == current.email:
            return current

        if value < str(current.phone_number):
            return self.search_recursive(current.left, value)
        else:
            return self.search_recursive(current.right, value)

    def delete(self, phone_number):
        self.root = self._delete_recursive(self.root, phone_number)

    def _delete_recursive(self, current, phone_number):
        if current is None:
            return current

        if phone_number < current.phone_number:
            current.left = self._delete_recursive(current.left, phone_number)
        elif phone_number > current.phone_number:
            current.right = self._delete_recursive(current.right, phone_number)
        else:
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left
            current.phone_number = self.min_value_node(current.right).phone_number
            current.right = self._delete_recursive(current.right, current.phone_number)

        return current

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self):
        result = []
        self.inorder_traversal_recursive(self.root, result)
        return result

    def inorder_traversal_recursive(self, current, result):
        if current:
            self.inorder_traversal_recursive(current.left, result)
            result.append((current.phone_number, current.name, current.email, current.password))
            self.inorder_traversal_recursive(current.right, result)

    def save_to_file(self):
        with open('data.txt', 'w') as file:
            self.save_to_file_recursive(self.root, file)

    def save_to_file_recursive(self, current, file):
        if current is not None:
            self.save_to_file_recursive(current.left, file)
            file.write(f"{current.name},{current.email},{current.password},{current.phone_number}\n")
            self.save_to_file_recursive(current.right, file)

    def load_from_file(self):
        try:
            with open('data.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(',')
                    if len(data) == 4:
                        name, email, password, phone_number = data
                        self.insert(name, email, password, int(phone_number))
        except FileNotFoundError:
            print("File not found.")


def email_format_checking(email):
    name_counter = 0
    for i in range(len(email)):
        if email[i] == '@':
            # print("Name End Here")
            break
        name_counter += 1

    email_name = email[0:name_counter]
    email_form = email[name_counter:]

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
        return False

    else:
        return True


def phone_format_checking(phone):
    ph_str = str(phone)
    num_counter:int = 0
    for i in range(len(ph_str)):
        if ph_str[0] == '9':
            num_counter += 1

    if num_counter == 10:
        return True
    else:
        return False


def strong_password_checking(password):
    special = 0
    numberChar = 0
    capChar = 0
    smallChar = 0
    pass_counter = len(password)
    if int(pass_counter) >= 8:
        for i in range(pass_counter):
            if 33 <= ord(password[i]) <= 42:
                special += 1
            elif 48 <= ord(password[i]) <= 57:
                numberChar += 1
            elif 65 <= ord(password[i]) <= 90:
                capChar += 1
            elif 97 <= ord(password[i]) <= 122:
                smallChar += 1

            if special > 0 and numberChar > 0 and capChar > 0 and smallChar > 0:
                return True
    return False

def create_user(node):
    name = input("Enter name: ")
    email = input("Enter email: ")
    if email_format_checking(email) is False:
        print("Email not valid")
        create_user(node)
    else:
        if node.is_email_unique(email) is False:
            print("Email already existed")
            create_user(node)
        else:
            password = input("Enter password: ")
            if strong_password_checking(password) is False:
                print("Your password is not strong. Please try again.")
                create_user(node)
            else:
                try:
                    phone_number = int(input("Enter phone number, +95: "))
                    if phone_format_checking(phone_number) is False:
                        print("Your phone is not valid")
                        create_user(node)
                    else:
                        if node.is_phone_unique(phone_number) is False:
                            print("Phone number already existed.")
                            create_user(node)
                        else:
                            node.insert(name, email, password, phone_number)
                            node.save_to_file()
                            print("User created.")
                except Exception as err:
                    print(err)


def read_all_data(node):
    # Perform an inorder traversal of the BST
    result = node.inorder_traversal()

    # Print all user data
    if result:
        for phone, name, email, password in result:
            print("Phone Number:", phone)
            print("Name:", name)
            print("Email:", email)
            print("Password:", password)
            print("---")
    else:
        print("Phonebook is empty.")


def update_user(node):
    value = input("Enter phone number or email to update: ")
    user = node.search(value)
    try:
        if user:
            name = user.name
            email = user.email
            password = user.password
            phone_number = user.phone_number

            choice = input(
                "User found.\nPress 1 to update name:\nPress 2 to update email:\nPress 3 to update password:\nPress 4 to phone number:\nPress 5 to exit:")
            if choice == '1':
                name = input(f"Enter new name ({user.name}): ")
            elif choice == '2':
                email = input(f"Enter new email ({user.email}): ")
                if email_format_checking(email) is False:
                    print("Email not valid")
                    update_user(node)
                else:
                    if node.is_email_unique(email) is False:
                        print("Email already existed")
                        update_user(node)
            elif choice == '3':
                password = input(f"Enter new password ({user.password}): ")
                if strong_password_checking(password) is False:
                    print("Your password is not strong enough. Try again")
                    update_user(node)
            elif choice == '4':
                phone_number = int(input(f"Enter new phone number ({user.phone_number}): "))
                if phone_format_checking(phone_number) is False:
                    print("Your phone number is not valid")
                    update_user(node)
                else:
                    if node.is_phone_unique(phone_number) is False:
                        print("Phone number is already existed.")
                        update_user(node)
            elif choice == '5':
                exit(0)
            else:
                print("Option not valid")
            node.delete(user.phone_number)
            node.insert(name, email, password, phone_number)
            node.save_to_file()
            print("User updated.")
        else:
            print("User not found.")
            update_user(node)
    except Exception as err:
        print("Option not valid, ", err)
        update_user(node)


def delete_user(node):
    value = input("Enter phone number or email to delete: ")
    user = node.search(value)
    if user:
        node.delete(user.phone_number)
        node.save_to_file()
        print("User deleted.")
    else:
        print("User not found.")


def search_user(node):
    value = input("Enter phone number or email to search: ")
    result = node.search(value)
    if result:
        print("Found:")
        print(f"Name: {result.name}")
        print(f"Email: {result.email}")
        print(f"Password: {result.password}")
        print(f"Phone Number: {result.phone_number}")
    else:
        print("User not found.")


if __name__ == "__main__":
    root_node = BST()
    root_node.load_from_file()
    while True:
        try:
            option = input(
                "Press 1 to create new cus acc:\nPress 2 to read cus info:\nPress 3 to update cus info:\nPress 4 to delete cus acc:\nPress 5 to find cus info:\nPress 6 to exit:")  # 1 is to add new data of cus
            # root_node =insert_data(10,root_node)
            if option == '1':
                create_user(root_node)
            elif option == '2':
                read_all_data(root_node)
            elif option == '3':
                update_user(root_node)
            elif option == '4':
                delete_user(root_node)
            elif option == '5':
                search_user(root_node)
            elif option == '6':
                exit(0)
            else:
                print("Option not valid!")
        except Exception as err:
            print("Option not valid ", err)
