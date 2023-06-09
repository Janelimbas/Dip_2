#getting all data on server with gad
import socket
import subprocess
import pymongo


#
# data = {"name":"kitty","email":"dkf1@gmail.com"}
# ids=collection.insert_one(data)
# print("ids",ids.inserted_id)

class TCPserver():

    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9898
        self.toSave = {}
        self.length = len(self.toSave)
        self.connection = pymongo.MongoClient("localhost", 27017)
        self.database = self.connection["ncc_test_dip2"]
        self.collection = self.database["user_info"]
        # self.collection.insert_one(self.toSave)

    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen()
        print("Server listen on port:{} and ip {}".format(self.server_port, self.server_ip))
        try:
            while True:
                client_conn, address = server.accept()
                print("Accepted Connection from - {} : {} ".format(address[0], address[1]))
                self.handle_client(client_conn)
        except Exception as err:
            print(err)

    def handle_client(self, client_socket):
        with client_socket as sock_conn:
            from_client = sock_conn.recv(1024)
            received_data = from_client.decode("utf-8")
            # print("Received Data From Client:", received_data)
            # print(type(received_data))

            print("Client sent : ", received_data)

            try:
                if received_data == "gad":
                    for i in self.collection.find():  # finding specific data on db
                        print("Data of db on server : ", i)

                else:
                    try:
                        output = subprocess.getoutput(received_data)
                        # result = output.stdout.decode()
                        output = subprocess.run(received_data, capture_output=True, shell=True)
                        result = output.returncode
                        client_cmd = output.stdout.decode('utf-8')
                        if result == 1:
                            print("Data received!")
                            message = "server got it:>" + received_data
                            to_send = bytes(message, 'utf-8')
                            sock_conn.send(to_send)
                        else:
                            print("*****************\n", client_cmd)
                            print("********************")
                            server_data = bytes(client_cmd, 'utf-8')
                            sock_conn.send(server_data)
                        # self.toSave = {"_id": self.length, "data": received_data}
                        self.toSave.update({"_id": self.length, "data": received_data})
                        self.length = self.length + 1
                        self.collection.insert_one(self.toSave)

                    except Exception as err:
                        print(err)
            except Exception as err:
                print(err)




if __name__ == '__main__':
    tcpserver = TCPserver()
    tcpserver.main()