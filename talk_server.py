import socket
import select
import argparse

print("Server bot welcomes you. Server bot is not lethal. Server bot does not record clients' personal data.")

parser = argparse.ArgumentParser(description="A prattle server")

parser.add_argument("-p", "--port", dest="port", type=int, default=12345,
                    help="TCP port the server is listening on (default 12345)")
parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                    help="turn verbose output on")
args = parser.parse_args()



def talk_server():
    port = args.port
    verbose = args.verbose
    
    while True:
        break

#//