import sys,os,time
prevPath = os.path.abspath(os.getcwd())
sys.path.insert(0,prevPath)
import jwt
from Modules.FaceRecognition import Recognition
import Modules.gaze_tracking
from Modules.Photo import takePhoto
from App.MongoDBConnection import db
import serial
from threading import Thread
import eel
eel.init('Panel')
#serial = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)



                           




@eel.expose
def jwtDecode(cookie):
    jwtSplit = cookie.split('=')[1]
    jwtSplit = (jwtSplit[2:]).replace('\'','')
    jwtResp = jwt.decode(jwtSplit, 'Hacklemigelkeklemi', algorithms=['HS256'])
    return jwtResp

@eel.expose
def setPhoto(userId):
    return takePhoto(userId)

def arduinoSerialRead():
    while  True:
        data = serial.readline().decode('UTF-8')
        if(data!=''):
            print(data)
            if('success' in data):
                eel.cardSaved()
            if('stored' in data):
                eel.setFingerMessage('saved')
            if('Remove finger' in data):
                eel.setFingerMessage('remove_and_press')

            


@eel.expose
def sendSerialData(userId):
    serial.write(userId.encode())



serialReadThread = Thread(target = arduinoSerialRead, args = ())
@eel.expose
def startSerialRead():
    serialReadThread.start()

eel.start('admin/dashboard.html',port=8001)

