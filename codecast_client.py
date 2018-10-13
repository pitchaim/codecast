import os, subprocess
import jack

if __name__ == "__main__":
    pass

class Client(self):


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

            #start jack client to manage connections
            jclient = jack.Client('JackClient')

            #wait for server to verify netjack RUNNING
            #look at ports, find incoming netjack channel,
            #route to system out, print something to cmd line!

    def runbash(self, cmd):
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output, error
