import select
from socket import *
import sys
import argparse
from _thread import *
import threading

def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 

DIVIDER = "\n=========================================╣\n"

parser = argparse.ArgumentParser(description="A prattle client")

parser.add_argument("-n", "--name", dest="name", type=str, default="machine name", help="name to be prepended in messages (default: machine name)")
parser.add_argument("-s", "--server", dest="server", default="127.0.0.1",
                    help="server hostname or IP address (default: 127.0.0.1)")
parser.add_argument("-p", "--port", dest="port", type=int, default=12345,
                    help="TCP port the server is listening on (default 12345)")
parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                    help="turn verbose output on")
args = parser.parse_args()

def runProgram():

    port = args.port
    verbose = args.verbose
    
    #socket initialization found at https://steelkiwi.com/blog/working-tcp-sockets/
    sock = socket(AF_INET, SOCK_STREAM)

    while True:
        try:
            sock.connect((args.server, args.port))
            sock.setblocking(0)
            break
        except:
            prRed("connection not established.")
            confirmation = input("       Try again? (y/n): ")

            if(confirmation == "n" or confirmation == "N"):
                return   

    start_new_thread(getMessages, (sock,))
    sendMessages(sock)
    sock.close()

        
def sendMessages(sock):

    name = args.name

    while True:
        incoming, outcoming, uhoh = select.select([sock], [sock], [sock], 1)

        userMessage = input()
        #userMessage += args.name
        userMessage = name + " says:" + userMessage

        #print(userMessage)
        print(DIVIDER)

        sock.send(userMessage.encode())

def getMessages(sock):
    while True:
        incoming, outcoming, uhoh = select.select([sock], [sock], [sock], 1)
        try:
            newMessg = sock.recv(1024).decode()
            print(newMessg + DIVIDER)
        except:
            yes = True

if __name__ == "__main__":
    runProgram()
