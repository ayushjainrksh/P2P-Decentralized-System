from libs import *
from server import Server
from client import Client


class p2p:
    peers = ['127.0.0.1']

def main():
    msg =  "Begin"
    while True:
        server = Server(msg)
        client = Client(p2p.peers[0])

if(__name__=="__main__"):
    main()