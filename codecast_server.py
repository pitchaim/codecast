import sys, os, subprocess
from socket import *
import ssl
from threading import Thread
import jack

class Server():

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

    def run(self):
        # ---SET UP SERVER SOCKET - LISTEN--- #
        # ---WHEN CONNECTION MADE, PROCEED--- #
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.settimeout(10)
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.ws = self.context.wrap_socket(self.s, server_side=True)
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

    def runbash(self, cmd):
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output, error

if __name__ == "__main__":

    # nice opening message
    print('\n')
    print('---------------------------------------')
    print('-----------C-O-D-E-C-A-S-T-------------')
    print('-----------------v1.0------------------')
    print('---------------------------------------')
    print('-------(c) Austin Marcus 2018----------')
    print('---------------------------------------')
    print('\n')

    # get password and server name from user
    sname = input('Desired server name: ')
    pw = input('Passphrase: ')

    # read in file with known clients
    # create Server instance, pass in password and client table
    # run server
    s = Server(pw, [], sname)
    s.run()
