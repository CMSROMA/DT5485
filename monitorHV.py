from DT5485Wrapper import DT5485
from time import sleep

c0=DT5485('/dev/dt5485_sn48')
c0.printID()

while(1):
    hvstatus=c0.getChStatus()
    vset=c0.getChVSET()
    vout=c0.getChVOUT()
    iout=c0.getChIOUT()
    print hvstatus,vset,vout,iout
