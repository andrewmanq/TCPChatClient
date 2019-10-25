import select
from socket import *
import sys
import argparse
from _thread import *
import threading
'''
  _        _ _           _ _            _   
 | |      | | |         | (_)          | |  
 | |_ __ _| | | __   ___| |_  ___ _ __ | |_ 
 | __/ _` | | |/ /  / __| | |/ _ \ '_ \| __|
 | || (_| | |   <  | (__| | |  __/ | | | |_ 
  \__\__,_|_|_|\_\  \___|_|_|\___|_| |_|\__|
               ______                      
              |______|    

ever wanted a more restricted and less feature-filled text messenger? we've got you covered.

This program connects with a server on a local port and sends text/string data while also being able to recieve messages from the server.
arguments:
-v = verbose
-s = server port
-p = port number
-n = your name (or not your name if you want to be secret)

Authors: Andrew Quist and Sambridhi Acharya
Written: Oct 25, 2019
'''

#code for printing red error words from https://www.geeksforgeeks.org/print-colors-python-terminal/
def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 

#This prints between every message.
DIVIDER = "\n________________________________________________________________\n"

#This block parses the arguments into readable data
parser = argparse.ArgumentParser(description="A prattle client")
parser.add_argument("-n", "--name", dest="name", type=str, default="machine name", help="name to be prepended in messages (default: machine name)")
parser.add_argument("-s", "--server", dest="server", default="127.0.0.1",
                    help="server hostname or IP address (default: 127.0.0.1)")
parser.add_argument("-p", "--port", dest="port", type=int, default=12345,
                    help="TCP port the server is listening on (default 12345)")
parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                    help="turn verbose output on")
args = parser.parse_args()

#A short bool that tells us whether or not to be verbose
v = args.verbose

#This is a variable that both threads check to make sure the other one is still running.
quit = False

'''
runProgram kickstarts the process of connecting to a server, and starts the threads that run the chat window.
'''
def runProgram():
    
    #socket initialization found at https://steelkiwi.com/blog/working-tcp-sockets/
    sock = socket(AF_INET, SOCK_STREAM)
    if v: prGreen("socket created.")

    #This block tries to connect to the previously designated server port. If it doesn't work, the program politely asks if you want to try to connect again.
    while True:
        try:
            #attempts to connect to socket
            sock.connect((args.server, args.port))
            if v: prGreen("socket connected.")
            sock.setblocking(0)
            break
        except:
            #failstate asks to try again
            prRed("connection not established.")
            confirmation = input("       Try again? (y/n): ")

            if(confirmation == "n" or confirmation == "N"):
                #this quits the program
                return   

    #This makes a new thread that checks the server for messages. The advantage of multithreading is that messages can come in even while the system is promting for input.
    start_new_thread(getMessages, (sock,))
    #Starts current thread on sending user messages.
    sendMessages(sock)
    #Closes the socket if the previous function is done
    sock.close()

''''
This is run in the main thread. It checks user input for messages and sends the message over to a server.
'''
def sendMessages(sock):

    quit = False
    name = args.name

    #This loops every time the system prompts for a new message. It is broken if something goes wrong.
    while True:

        try:
            #checks if the server is ready to write
            ready = select.select([sock], [sock], [sock], 3)

            #https://pymotw.com/2/select/
            if not (ready[0] or ready[1]):
                prRed("Connection timed out. Quitting...")
                quit = True
                break
            
            #gets an input from the command line
            userMessage = input()
            #prepends our name onto the message sent to the server
            userMessage = name + " says:" + userMessage

            #print(userMessage)
            print(DIVIDER)

            #encodes the string to send to a server
            if v : prGreen("sending message.")
            sock.send(userMessage.encode())
            if v : prGreen("message sent.")

            if quit:
                break
        except:
            #A catch-all for problems during information transmission. This diagnoses the issue and closes the thread.
            prRed("There was a problem sending your message. Closing thread...")
            quit = True
            break

''''
This is run in a new thread. It checks server output and prints out incoming messages.
'''
def getMessages(sock):

    if v: prGreen("Message recieving thread created.")

    quit = False
    while True:

        try:
            #checks if server is ready to read
            ready = select.select([sock], [sock], [sock], 3)

            #https://pymotw.com/2/select/
            if not (ready[0] or ready[1]):
                prRed("Connection timed out. Quitting...")
                quit = True
                break
                
            try:
                #recieve a new message
                newMessg = sock.recv(1024).decode()
                #closed servers send empty messages. This code avoids that
                if newMessg == "":
                    prRed("network not availible. Press ctrl-c to quit.")
                    quit = True
                    break
                if v: prGreen("message recieved.")
                print(newMessg + DIVIDER)
            except:
                #blank statement - unoffensive
                yes = True
            
            if(quit):
                break
        except:
            #A catch-all for problems during information transmission. This diagnoses the issue and closes the thread.
            prRed("There was a problem recieving messages. Closing thread...")
            quit = True
            break

if __name__ == "__main__":
    #run that program!
    runProgram()
