import npyscreen
from DT5485Wrapper import DT5485
import csv
import time

class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", DT5485ControlPanel, name="DT5485 Control Panel V1.0 by PM")

class DT5485ControlPanel(npyscreen.ActionForm):
    # Constructor
    def create(self):
        self.OK_BUTTON_TEXT='Apply'
        self.CANCEL_BUTTON_TEXT='Exit'
        self.__class__.CANCEL_BUTTON_BR_OFFSET = (2, 15)

        # Add the TitleText widget to the form
        self.port = self.add(npyscreen.TitleText, name="BOARD", value="/dev/dt5485_sn48", editable=False)
        self.dt5485 = DT5485(self.port.value)
        self.idString =  self.add(npyscreen.TitleText, name="BOARD ID", value="****  %s ID %d S/N %d   ****"%(self.dt5485.model,self.dt5485.product, self.dt5485.sn), editable=False)
        self.chStatus = self.dt5485.getChStatus()
        self.switch = self.add(npyscreen.Checkbox, name = "ON/OFF", scroll_exit=True)
        if (self.chStatus):
            self.switch.value=True
        else:
            self.switch.value=False
        self.vset_target=self.dt5485.getChVSET()
        self.vset = self.add(npyscreen.TitleText, name="VSET [20-80]:", value=str(self.vset_target))
        self.vmon = self.add(npyscreen.TitleText, name="VMON        :", value="", editable=False)
        self.imon = self.add(npyscreen.TitleText, name="IMON        :", value="", editable=False)
        self.monitorSwitch = self.add(npyscreen.Checkbox, name = "Write to file", scroll_exit=True)
        self.writeToFile = self.monitorSwitch.value
        self.outputFilename = self.add(npyscreen.TitleFilename, name="Output file:", value="test.csv")
#        self.parentApp.setNextForm(None)

    def on_ok(self):
        if (float(self.vset.value)>80.):
            self.vset.value=str(80)
        if (float(self.vset.value)<20.):
            self.vset.value=str(20)

        if (abs(float(self.vset.value) - self.vset_target)>0.01):
            r=self.dt5485.setChVSET(float(self.vset.value))
            if (r==0):
                self.vset_target=float(self.vset.value)
            else:
                self.vset.value='Error setting VSET'
                
        if (self.switch.value != self.chStatus):
            if (self.switch.value):
                r=self.dt5485.setRegister(0,1)
            else:
                r=self.dt5485.setRegister(0,0)
            if (r==0):
                self.chStatus=self.switch.value 
            else:
                self.vset.value='Error switching channel'

        if (self.monitorSwitch.value != self.writeToFile):
            if (self.monitorSwitch.value):
                self.outputFile=open(str(self.outputFilename.value), mode='w+') 
                self.csvWriter = csv.writer(self.outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                self.writeToFile = self.monitorSwitch.value
            else:
                self.writeToFile = self.monitorSwitch.value

    def while_waiting(self):
        vout=self.dt5485.getChVOUT()
        iout=self.dt5485.getChIOUT()
        self.vmon.value="%5.3f V"%vout
        self.imon.value="%5.3f muA"%(iout*1000)
        self.vmon.display()
        self.imon.display()
        if (self.writeToFile):
            self.csvWriter.writerow([str(int(self.chStatus)),str(self.vset_target),str(vout),str(iout),str(time.time())])
#       
#        Only here change the
    # Override method that triggers when you click the "cancel"
    def on_cancel(self):
        self.parentApp.setNextForm(None)
        if (self.writeToFile):
            self.outputFile.close()

MyApp = App()
MyApp.run()
