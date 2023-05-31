
import socket
import subprocess
import os

class TCPserver():
    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9988
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
        with client_socket as sock:
            from_client = sock.recv(1024)
            received_data = from_client.decode("utf-8")
            # print("Received Data From Client:", received_data)

            print("Client sent : ", received_data)

            try:
                output = subprocess.getoutput(received_data)

                # result = output.stdout.decode()
                output = subprocess.run(received_data, capture_output=True, shell=True)
                result = output.returncode
                client_cmd = output.stdout.decode('utf-8')
                if result == 1:
                    print("Data received!")
                    # self.toSave.update(received_data)
                    message = "server got it:>" + received_data
                    to_send = bytes(message, 'utf-8')
                    sock.send(to_send)
                else:
                    # return_valued = os.system(received_data)
                    print("*****************\n",client_cmd )
                    print("********************")
                    server_data = bytes(client_cmd,'utf-8')
                    sock.send(server_data)

            except Exception as err:
                print(err)


if __name__ == '__main__':
    tcpserver = TCPserver()
    tcpserver.main()