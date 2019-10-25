from libs import *

class Server:

    def __init__(self,msg):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.connections = []
        self.peers = []
        
        self.listen_socket.bind((HOST, PORT))
        self.listen_socket.listen(1)

        print(f'Serving HTTP on port {PORT} ...')
        
        self.run()

    
    def run(self):
        while True:
            client_connection, client_address = self.listen_socket.accept()
            
            self.peers.append(client_address)
            print(self.peers)
            self.send_peers()

            self.connections.append(client_connection)
            print(client_connection, " added")

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
            listOfPeers += str(peer[0])+", "
        
        for connection in self.connections:
            data  =  '\x11' + bytes(listOfPeers, 'utf-8')
            connection.send('\x11' + bytes(listOfPeers, 'utf-8'))
# server = Server("HELLO")