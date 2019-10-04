from DT5485Wrapper import DT5485

c0=DT5485('/dev/dt5485_sn48')
c0.printID()

hvONOFF=c0.getChStatus()
print "CH0 status is "+str(hvONOFF)

mode=c0.getChMode()
print "CH0 mode is "+str(mode)

vset=c0.getChVSET()
print "CH0 VSET is "+str(vset)

print "Setting VSET @35V"
r=c0.setChVSET(35.)
vset=c0.getChVSET()
print "CH0 VSET is "+str(vset)

print "Turning CH0 ON"
r=c0.setRegister(0,1)
hvONOFF=c0.getChStatus()
print "CH0 status is "+str(hvONOFF)

for i in range(0,50):
    vout=c0.getChVOUT()
    iout=c0.getChIOUT()
    print vout,iout

print "Turning CH0 OFF"
r=c0.setRegister(0,0)

for i in range(0,50):
    vout=c0.getChVOUT()
    iout=c0.getChIOUT()
    print vout,iout

hvONOFF=c0.getChStatus()
print "CH0 status is "+str(hvONOFF)
