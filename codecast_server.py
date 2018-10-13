import sys, os, subprocess
from socket import *
import ssl
from thread import thread
from Crypto.Cipher import AES
import jack

if __name__ == "__main__":
    # command-line arg: name you want people to see for this stream
    sname = sys.argv[1]
    # read in file with known clients
    # create Server instance, pass in password and client table
    # run server

class Server(self):

    def __init__(self, password, client_table, sname):
        self.password = password
        self.client_table = client_table
        self.sname = sname
        self.max_clients = len(client_table)
        self.HOST = ""
        self.PORT = 15224

        # connection status flags
        self.START = 0
        self.CHECKED_PW = 1

        self.client = jack.Client('JackClient')

        # nice opening message
        print('\n')
        print('---------------------------------------')
        print('-----------C-O-D-E-C-A-S-T-------------')
        print('-----------------v1.0------------------')
        print('---------------------------------------')
        print('-------(c) Austin Marcus 2018----------')
        print('---------------------------------------')
        print('\n')


    def run(self):
        # ---SET UP SERVER SOCKET - LISTEN--- #
        # ---WHEN CONNECTION MADE, PROCEED--- #
        self.s = socket(AF_INET, SOCK_STREAM)
        self.context = ssl.create_default_context()
        self.ws = self.context.wrap_socket(self.s, ssl_version=ssl._PROTOCOL_SSLv23, ciphers="ADH-AES256-SHA")
        self.ws.bind((self.HOST, self.PORT))
        self.ws.listen(self.max_clients)
        print('Server running')
        for i in range(self.max_clients):
            Thread(target=self.clientHandler).start()

    def clientHandler(self):
        # reqIP = requester IP from SOCKET
        # cmd = 'jack_netsource -H {}'.format(reqIP)
        # runbash(cmd)
        # send message over socket that netjack RUNNING,
        # maybe include a message to display at
        # client cmd line
        status = self.START
        conn, addr = self.s.accept()
        cname = addr
        print('Got connection request from {}'.format(addr))
        while 1:
            data = conn.recv(1024)
            if not data:
                break
            msg = repr(data)
            if status == self.START:
                #first step - check password
                msg_c = msg.split()
                if len(msg_c) == 2:
                    cname = msg_c[1]
                if msg[0] == self.password:
                    print('Correct password - setting up Jack connection with {}'.format(cname))
                    cmd = 'jack_netsource -H {}'.format(cname)
                    output,error = self.runbash(cmd)
                    # check if any issues setting up netjack connection
                    if len(error) == 0:
                        conf_msg = 'CORRECT RUNNING {}'.format(self.sname)
                    else:
                        conf_msg = 'CORRECT NETJACK ERROR'
                    conn.send(conf_msg)
                    status = self.CHECKED_PW
                else:
                    # wrong password - deny connection
                    print('Wrong password - closing connection with {}'.format(cname))
                    deny_msg = 'INCORRECT CLOSING CONNECTION'
                    conn.send(deny_msg)
                    conn.close()
            elif status == self.CHECKED_PW:
                # if password already checked, either jack is connected or not;
                # either way, only thing to do is close connection if client requests
                if msg == 'CLOSE':
                    print('Client {} closed connection'.format(cname))
                    conn.close()

    def do_encrypt(self, message, password):
        obj = AES.new(password, AES.MODE_CBC)
        cipher = obj.encrypt(message)
        return cipher

    def runbash(self, cmd):
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output, error
