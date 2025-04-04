import threading 
import socket
import argparse
import os 
import sys

class Send(threading.Thread):
    #Listens for user input from the command line

    #sock the connected sock object
    #name (str) : The username provided by the user

    def __init__(self, sock, name):

        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
       #Listens for user input from the command line and send it to the server.
       #Typing Quit will close the connection and exit the app

        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            #if we type "QUIT" we leave the chatroom
            if message == 'QUIT':
                self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
                break
            #send message to the server for broadcasting
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))
            
        print('\nQuitting...')
        self.sock.close()
        os._exit(0)

class Receive(threading.Thread):
    #Listens for incoming messages from the server
    def __init__(self, sock, name):

        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):
        #Receives data from the server and displays it in the console
        while True:
            message = self.sock.recv(1024).decode('ascii')
            if message:
                if self.messages:
                    print('...')
                    print('\r{}\n{}: '.format(message, self.name), end='')
                else:
                    print('\r{}\n{}: '.format(message, self.name), end='')
            else:
                print('\nDisconnected from server')
                print('Quitting...')
                self.sock.close()
                os._exit(0)

class Client:
    #Managment of client-server connection and integration of GUI

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None

    def start(self):
        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Successfully connected to {}:{}'.format(self.host, self.port))

        print()
        self.name = input('Your name: ')
        print()
        print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

        # Create send and receive threads

        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        send.start()
        receive.start()

        self.sock.sendall('Server: {} has joined the chat.'.format(self.name).encode('ascii'))

        print("\rReady! Leave the chatroom anytime by typing 'QUIT'.\n")
        print('{}: '.format(self.name), end='')

        return receive
    


def main(host, port):
    client = Client(host, port)
    client.start()

   


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument("host", help="Interface the server listens at")
    parser.add_argument("-p", metavar="PORT", type=int, default=1060, help="TCP port (default 1060)")

    args = parser.parse_args()

    main(args.host, args.p)