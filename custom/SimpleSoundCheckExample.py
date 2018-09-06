#SoundCheck TCP Control Example v1.0
#SoundCheck 15.0 (or greater) must be open and running before executing this script.
#SoundCheck must have TCP/IP server enabled on port 4444 
#Sends simple commands to SoundCheck via TCP, and receives responses as JSON strings
#
#Python 3.x compatible
#Requires json
#
# # start
# sudo launchctl load /Library/LaunchDaemons/org.jenkins-ci.plist
#
# # stop
# sudo launchctl unload /Library/LaunchDaemons/org.jenkins-ci.plist

import socket
import array
import sys
import json

#check to see whether pylab plotting software is installed locally
try:
    from pylab import *
    found_pylab = True
except:
    found_pylab = False

#Declare SoundCheckTcp class

class SoundCheckTcp:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.connect((self.ip, self.port))
        self.sock.recv(500) # This should be the Welcome message

    #define command send/receive method for simplified call

    def send(self, cmd):
        cmd_ba = bytearray("%s\r\n" % cmd, "utf8")
        self.sock.send(cmd_ba)
        #data = read_for_a_while(self.sock)
        data = self.sock.recv(100000)
        js = json.loads((data).decode("utf8"))
        if js["cmdCompleted"]:
            return js
        else:
            raise Exception("SoundCheck command did not complete:  %s: %s: %s: %s" % (js["errorDescription"], js["errorType"], js["originalCommand"], data))

    def open(self, filename):
        self.send("Sequence.Open('%s')" % filename)

    def setLotNumber(self, lotNumber):
        self.send("SoundCheck.SetLotNumber('%s')" % lotNumber)

    def getLotNumber(self):
        js = self.send("SoundCheck.GetLotNumber")
        return js["returnData"]["Value"]

    def setLoginLevel(self, level="engr"):
        js = self.send("SoundCheck.SetLoginLevel('%s')" % level)

    def getLoginLevel(self):
        js = self.send("SoundCheck.GetLoginLevel")
        return js["returnData"]["Value"]

    def memGetAllNames(self):
        js = self.send("MemoryList.GetAllNames")
        return js["returnData"]
        
    def run(self):
        js = self.send("Sequence.Run")
        return js["returnData"]["Pass?"]

    def getCurveNames(self):
        return self.memGetAllNames()["Curves"]
    
    def getWaveformNames(self):
        return self.memGetAllNames()["Waveforms"]
    
    def getValueNames(self):
        return self.memGetAllNames()["Values"]
    
    def getResultNames(self):
        return self.memGetAllNames()["Results"]

    def get(self, gtype, name):
        js = self.send("MemoryList.Get('%s', '%s')" % (gtype, name))
        return js["returnData"]
    
    def getCurve(self, name):
        return self.get('Curve', name)
    
    def getWaveform(self, name):
        return self.get('Waveform', name)
    
    def getValue(self, name):
        return self.get('Value', name)
    
    def getResult(self, name):
        return self.get('Result', name)
    
    def __del__(self):
        self.sock.close()
        
sc = SoundCheckTcp("0.0.0.0", 4444)


print("\n\nOpening sequence")
sc.open("c:/SoundCheck 15.0-x64/Sequences/Loudspeakers/Complete Test.sqc")

print("\n\nRunning open sequence")
RunResult = sc.run()

print("Sequence run result: %s" % RunResult)

print("\n\nSetting lot number")
sc.setLotNumber("1234")
print("\n\nLot number is %s" % sc.getLotNumber())

print("Login level is %s" % sc.getLoginLevel())
names = sc.memGetAllNames()

curveNames = sc.getCurveNames()
print("Here are the curve names:")
print("\n	".join(curveNames))

#Get Fundamental curve from memory list
fundamental = sc.getCurve("Fundamental")
print("%s" % fundamental)


#try plotting Fundamental curve
if found_pylab:
    # Plotting raw curve data points
    plot(fundamental["Curve"]["XData"],
         fundamental["Curve"]["YData"])
    grid()
    title("Fundamental")
    
    #set limits based on data max/min, looks better than autoscale
    xlim(min(fundamental["Curve"]["XData"]),max(fundamental["Curve"]["XData"])+1000 )
    ylim(min(fundamental["Curve"]["YData"])-3,max(fundamental["Curve"]["YData"])+3)

    #set axis labels
    ylabel(fundamental["Curve"]["YDataScale"])
    xlabel(fundamental["Curve"]["XUnit"])

    #set scale format
    yscale('Linear')
    xscale('Log')
    show()

