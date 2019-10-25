from libs import *

class Client:

    def __init__(self, addr):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.connect((addr, PORT))
        # self.listen_socket.listen(1)

        # print(f'Serving HTTP on port {PORT} ...')
        i_thread = threading.Thread(target=self.send_message)
        i_thread.daemon = True
        i_thread.start()

        while True:

            r_thread = threading.Thread(target=self.receive_message)
            r_thread.start()
            r_thread.join()

            data = self.receive_message()

            if not data:
                print("Server failed")
                break

            elif data[0:1]  == b'\x11':
                print("Got peers")
                self.update_peers(data[1:])
                print(data)

    def send_message(self):
        try:
            self.listen_socket.send("req".encode('utf-8'))

        except KeyboardInterrupt:
            self.send_disconnect_signal()
            return


    def receive_message(self):
        try:
            print("Receiving...")
            data = self.listen_socket.recv(1024)
            print("Received message is : ")
            print(data.decode('utf-8'))
            return data
        except KeyboardInterrupt:
            self.send_disconnect_signal()

    def update_peers(self, peers):
        print("--------  ", peers)
        print("YO : ", p2p.peers)
        p2p.peers = str(peers, "utf-8").split(',')[:-1]


    def send_disconnect_signal(self):
        print("Disconnected from server")
        self.listen_socket.send("q".encode('utf-8'))
        sys.exit()