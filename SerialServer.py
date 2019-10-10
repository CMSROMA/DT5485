import zmq
import serial
from time import sleep

class SerialServer:
    def __init__(self,port,device):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:%d"%port)
        self.serial = serial.Serial(device, 115200,timeout=0)
        print("SerialServer listening at *:%d relaying to %s" % (port,device))

    def loop(self):
        while True:
            msg = self.socket.recv()
#            print("Processing %s" % msg.decode("utf-8").strip())
            self.serial.write(msg)
            sleep(0.2)
            reply=self.serial.readline().strip()
            self.socket.send(reply.encode())

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-p","--port")
parser.add_option("-d","--device")
(options,args)=parser.parse_args()

myServer = SerialServer(int(options.port),options.device)
myServer.loop()
