from libs import *

class Client:

    def __init__(self, addr):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.connect((addr, PORT))
        self.listen_socket.listen(1)

        # print(f'Serving HTTP on port {PORT} ...')
        
        while True:
            data = self.receive_message()

            if not data:
                print("Server failed")
                break

            elif data[0:1]   == b'\x11':
                print("Got peers")
                print(data)

    def receive_message(self):
        print("Receiving...")
        data = self.listen_socket.recv(1024)
        print(data.decode('utf-8'))
        print("Received message is : ")
        return data