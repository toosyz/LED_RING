# Basic Python Plugin Example
#
# Author: GizMoCuz
#
"""
<plugin key="RGBString" name="RGB Strip or Ring" author="toosyz" version="1.0.0" wikilink="" externallink="">
    <description>
        <ul style="list-style-type:square">
            <li>Enter colors in the following format: given in hex code and seperated by semicolons</li>
            <li>Website for acquiring hex coded colors: https://www.color-hex.com/</li>
            <li>Speed of rotation: the amount of seconds it takes for a single color to pass through each led and return to its original state.</li>
            <li>If the formatting of the colors or the speed of rotation is wrong, the given values will be ignored in creating the output.</li>
        </ul>
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="30px" required="true" default="9090"/>
        <param field="Mode1" label="Custom Colours" width="200px" default=""/>
        <param field="Mode2" label="Speed of rotation (note: value ignored if movement not set to rotation" width="200px">
            <options>
                <option label="No rotation" value="0"/>
                <option label="Very Slow" value="1"/>               
                <option label="Slow" value="2"/>
                <option label="An Okay Speed" value="3"/>
                <option label="Fast" value="4"/>
                <option label="Very fast" value="5" default="0"/>
            </options>
        </param>
        <param field="Mode5" label="Speed of blinking" width="200px">
            <options>
                <option label="No Blinking" value="0"/>
                <option label="Very Slow" value="1"/>               
                <option label="Slow" value="2"/>
                <option label="An Okay Speed" value="3"/>
                <option label="Fast" value="4"/>
                <option label="Very fast" value="5" default="0"/>
            </options>
        </param>
        <param field="Mode3" label="First colour" width="200px">
            <options>
                <option label="Yellow" value="ffff00"/>
                <option label="Orange Yellow" value="f8d568"/>
                <option label="Orange" value="ffa500"/>
                <option label="Orange Red" value="ff4500"/>
                <option label="Red" value="ff0000"/>
                <option label="Red Purple" value="8a2be2"/>
                <option label="Purple" value="800080"/>
                <option label="Blue Purple" value="8a2be2"/>
                <option label="Blue" value="0000ff"/>
                <option label="Blue Green" value="0d98ba"/>
                <option label="Green" value="00ff00"/>
                <option label="Yellow Green" value="9acd32" default="0d98ba"/>
            </options>
        </param>
        <param field="Mode4" label="Second colour" width="200px">
            <options>
                <option label="Yellow" value="ffff00"/>
                <option label="Orange Yellow" value="f8d568"/>
                <option label="Orange" value="ffa500"/>
                <option label="Orange Red" value="ff4500"/>
                <option label="Red" value="ff0000"/>
                <option label="Red Purple" value="8a2be2"/>
                <option label="Purple" value="800080"/>
                <option label="Blue Purple" value="8a2be2"/>
                <option label="Blue" value="0000ff"/>
                <option label="Blue Green" value="0d98ba"/>
                <option label="Green" value="00ff00"/>
                <option label="Yellow Green" value="9acd32" default="8a2be2"/>
            </options>
        </param>
        <param field="Mode6" label="Pattern" width="200px">
            <options>
                <option label="Repetition (of custom values)" value="1"/>
                <option label="Gradient (of first and second colour)" value="2"/>
                <option label="High on lsd (all other values ignored)" value="3" default="1"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz

class BasePlugin:
    myConn=None
    LEDCOUNT=8 #max 99
    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        self.myConn = Domoticz.Connection(Name="Hyperion", Transport="TCP/IP", Protocol="None", Address=Parameters["Address"], Port=Parameters["Port"])
        self.myConn.Connect()        
           
    def onStop(self):
        Domoticz.Log("onStop called")
        self.myConn.Disconnect()

    def onConnect(self, Connection, Status, Description):
        commandString="99"+ Parameters["Mode2"]+ Parameters["Mode5"] #sending command on movement
        #SENDING instructions on rotation and blinking
        self.myConn.Send("0;0;1;1;40;"+commandString+"\n")
        
        #checking for what kind of pattern is set
        
        if Parameters["Mode6"]=="1": #for when we want repeptition
            colorArray=Parameters["Mode1"].split(';')
            for i in range(len(colorArray)):
                if colorArray[len(colorArray)-i-1]=="":
                    colorArray.remove(colorArray[len(colorArray)-i-1])
            for j in range(len(colorArray)):
                int(colorArray[j], 16) #this will be runtime error, if given value is not well formatted
            if len(colorArray)!=0:
                for k in range(self.LEDCOUNT):
                    ledNumber=None
                    if(self.LEDCOUNT<10):
                        ledNumber="0"+str(k)
                    else:
                        ledNumber=str(k)
                    colorToSend=colorArray[k%len(colorArray)]
                    self.myConn.Send("0;0;1;1;40;"+ledNumber+""+colorToSend+"\n")
                
        elif Parameters["Mode6"]=="2": #for when we want a gradient
            startColor = int(Parameters["Mode3"], 16)
            endColor=int(Parameters["Mode4"], 16)
            ledNumber=None
            for x in range(self.LEDCOUNT):
                temp=str(hex(startColor+(endColor-startColor)*x//self.LEDCOUNT))
                temp=temp[2:]
                for y in range(6-len(temp)):
                    temp="0"+temp
                if x<10:
                    ledNumber="0"+str(x)
                else:
                    ledNumber=str(x)
                self.myConn.Send("0;0;1;1;40;"+ledNumber+""+temp+"\n")
            Domoticz.Log("0;0;1;1;40;"+ledNumber+""+temp)
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

