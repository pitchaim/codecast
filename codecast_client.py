import os, subprocess
from socket import *
from threading import Thread
import jack

if __name__ == "__main__":
    pass

class Client():


    def __init__(self):
        #@todo:
        # ---ESTABLISH SOCKET CONNECTION WITH SERVER--- #
        #       ---ONCE ESTABLISHED, PROCEED---         #

        #slave - open jackd with net backend
        cmd0 = 'ijo=$(ps -ef | grep jackd); if [[ $ijo == *"/jackd"* ]]; then echo "RUNNING"; fi'
        output, error = self.runbash(cmd0)
        if not output[0] == 'RUNNING':
            cmd = 'jackd -R -d net'
            output, error = self.runbash(cmd)
        else:
            cmd = 'jackd -d net'
            output, error = self.runbash(cmd)
            #ISSUE: maybe doesn't work without -R realtime flag?

        #start jack client to manage connections
        jclient = jack.Client('JackClient')

        #wait for server to verify netjack RUNNING
        #look at ports, find incoming netjack channel,
        #name of net port will have some identifying label -
        #figure it out ... here pretend it's TOKEN
        net_in_p = jclient.get_ports('*TOKEN*')
        sys_out_p = jclient.get_ports('system:playback_*')
        # connect net_in_p to system out

        #print something to cmd line - hostname, time up, messages
        #passed through socket, etc.

    def runbash(self, cmd):
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output, error
