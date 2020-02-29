import serial
from time import sleep
from SerialClient import serialClient
class DT5485:
    def __init__(self,port):
        self.port=port
        if ('tcp://' in port):
            self.serial = serialClient(port)
        else:
            self.serial = serial.Serial(port, 115200,timeout=0)

        self.serial.write('AT+MACHINE\r\n')
        sleep(0.1)
        r=self.serial.readline().strip()
        self.serial.write('AT+CGMI\r\n')
        sleep(0.1)
        self.manufacturer=self.serial.readline().strip()
        self.serial.write('AT+CGMM\r\n')
        sleep(0.1)
        self.model=self.serial.readline().strip()
        self.sn=int(self.getRegister(254))
        self.product=int(self.getRegister(251))
        self.hwver=float(self.getRegister(253))
        self.fwver=float(self.getRegister(252))

    def printID(self):
        print "***********************************************************"
        print "****  %s ID %d S/N %d at port %s    ****"%(self.model,self.product, self.sn, self.port)
        print "****  HW Ver: %f       -      FW Ver %f    ****"%(self.hwver,self.fwver)
        print "***********************************************************"

    def getRegister(self,register):
        r=''
        while not 'OK=' in r:
            self.serial.write('AT+GET,%d\r\n'%register)
            sleep(0.2)
            r=self.serial.readline().strip()
        r=r.replace('OK=','')
        return r

    def setRegister(self,register,value):
        if (type(value) == int):
            self.serial.write('AT+SET,%d,%d\r\n'%(register,value))
        elif (type(value) == float):
            self.serial.write('AT+SET,%d,%f\r\n'%(register,value))
        else:
            print "Only integer or float registers are allowed"
            return -1
        sleep(1)
        r=self.serial.readline().strip()
        if not 'OK' in r:
            print 'Error: Unknown response '+r
            return 1
        return 0

    def getChStatus(self):
        r=self.getRegister(0)
        if ( r == 'false' ):
            return 0
        elif ( r == 'true' ):
            return 1
        else:
            return -1

    def getChMode(self):
        r=int(self.getRegister(1))
        return r

    def setChMode(self):
        r=self.setRegister(1,value)
        return r

    def getChVSET(self):
        r=float(self.getRegister(2))
        return r

    def setChVSET(self,value):
        r=self.setRegister(2,value)
        return r

    def getChVMAX(self):
        r=float(self.getRegister(4))
        return r

    def setChVMAX(self,value):
        r=self.setRegister(4,value)
        return r

    def getChIMAX(self):
        r=float(self.getRegister(6))
        return r

    def setChIMAX(self,value):
        r=self.setRegister(6,value)
        return r

    def getChVOUT(self):
        r=float(self.getRegister(231))
        return r

    def getChIOUT(self):
        r=float(self.getRegister(232))
        return r

    def getChTEMP(self):
        r=float(self.getRegister(234))
        return r

    def getChTCOEFF(self):
        r=float(self.getRegister(28))
        return r

    def setChTCOEFF(self,value):
        r=self.setRegister(28,value)
        return r

    def saveCurrentConfig(self):
        r=self.setRegister(255,1)
        return r

    def emergencyStop(self):
        r=self.setRegister(31,1)
        return r

     
