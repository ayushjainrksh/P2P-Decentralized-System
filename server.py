from libs import *

class Server:

    def __init__(self,msg):
        try:
            self.msg = msg
            self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.connections = []
            self.peers = []
            
            self.listen_socket.bind((HOST, PORT))
            self.listen_socket.listen(3)

            print(f'Serving HTTP on port {PORT} ...')
            
            self.run()

        except KeyboardInterrupt:
            print("Disconnected")
            sys.exit()

    def handler(self, client_connection, client_address):
        try: 
            while True:

                data = client_connection.recv(1024)
                print(data.decode('utf-8'))
                for connection in self.connections:
                    # print(connection)
                    if data and data.decode('utf-8')[0].lower == 'q':
                        self.disconnect(connection, client_address)
                        return
                    
                    elif data and data.decode('utf-8') == "req":
                        print("Uploading")
                        connection.send(self.msg.encode('utf-8'))
                        return
                        
        except KeyboardInterrupt:
            sys.exit()

    def disconnect(self, client_connection, client_address):
        self.connections.remove(client_connection)
        self.peers.remove(client_address)
        client_connection.close()
        self.send_peers()
        print("{}, disconnected".format(client_address))


    
    def run(self):

        while True:
            client_connection, client_address = self.listen_socket.accept()
            
            self.peers.append(client_address)
            print("Peers : ", self.peers)
            self.send_peers()
            
            c_thread = threading.Thread(target=self.handler, args=(client_connection, client_address))
            c_thread.daemon = True
            c_thread.start()

            self.connections.append(client_connection)
            print("{}, connected".format(client_address))

        #     request_data = client_connection.recv(1024)
        #     print(request_data.decode('utf-8'))
        #     http_response = b"""\
        # HTTP/1.1 200 OK

        # Hello, World!
        # """
            # client_connection.sendall(http_response)
            # client_connection.close()

    def send_peers(self):
        listOfPeers = ""
        for peer in self.peers:
            # print("- -- -", peer[0], "- -- -")
            listOfPeers = listOfPeers + str(peer[0]) + ", "
        # print("----", listOfPeers, "----")

        for connection in self.connections:
            data  =  b'\x11' + bytes(listOfPeers, 'utf-8')
            connection.send(b'\x11' + bytes(listOfPeers, 'utf-8'))
            print(data)
            print(connection)
# server = Server("HELLO")