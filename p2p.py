from libs import *
from server import Server
from client import Client


class p2p:
    peers = ['127.0.0.1']

def main():
    msg =  "Begin"
    while True:

        time.sleep(randint(1,2))

        for peer in p2p.peers:
            try:
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
               pass 

            try:
                server = Server(msg)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
               pass

if(__name__=="__main__"):
    main()