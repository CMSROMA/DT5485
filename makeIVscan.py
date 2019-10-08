from DT5485Wrapper import DT5485
from time import sleep

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-p","--port")
parser.add_option("-m","--vmin")
parser.add_option("-M","--vmax")
parser.add_option("-s","--vstep")
parser.add_option("-n","--nmeas")
parser.add_option("-o","--out")
(options,args)=parser.parse_args()

c0=DT5485(options.port)
c0.printID()

vmin=float(options.vmin)
vmax=float(options.vmax)
vstep=float(options.vstep)
nmeas=int(options.nmeas)

hvONOFF=c0.getChStatus()
if (hvONOFF>0):
    r=c0.setRegister(0,0)
    hvONOFF=c0.getChStatus()
    print "Waiting for CH0 to be off"
    while (hvONOFF!=0):
        hvONOFF=c0.getChStatus()
        sleep(1)
        print "Retrying"

print "Setting VSET @"+str(vmin)
r=c0.setChVSET(vmin)
vset=c0.getChVSET()
if (vset != vmin):
    print "Cannot set VSET to "+vmin
    exit(-1)

print "Turning CH0 ON"
r=c0.setRegister(0,1)


import csv

outFile=open(options.out, mode='w+') 
csvWriter = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
print "Writing data to "+options.out

while (vset<=vmax):
    sleep(5)
    print "VSET@"+str(vset)+" V"
    for i in range(0,nmeas):
        vout=c0.getChVOUT()
        iout=c0.getChIOUT()
        csvWriter.writerow([str(vset),str(vout),str(iout)])
        print "%f,%f,%f"%(vset,vout,iout)
    vset+=vstep
    r=c0.setChVSET(vset)
    if (r!=0):
        print "Problems setting VSET"

outFile.close()
    
print "Turning CH0 OFF"
r=c0.setRegister(0,0)
hvONOFF=c0.getChStatus()
print "Waiting for CH0 to be off"
while (hvONOFF!=0):
    hvONOFF=c0.getChStatus()
    sleep(1)
    print "Retrying"
