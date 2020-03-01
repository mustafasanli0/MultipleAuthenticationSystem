import sys,os
prevPath = os.path.abspath(os.getcwd())
sys.path.insert(0,prevPath)

from Modules.FaceRecognition import Recognition
import Modules.gaze_tracking
from App.MongoDBConnection import db
import eel
from threading import Thread
import serial
serial = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)


eel.init('Panel')

@eel.expose
def getEntries():
    entries = db.entries.aggregate([
    {"$project": {"_id": { "$toString": "$_id" }, 'entry':1 } }
    ])
    return list(entries)


response = {}

def faceRecognition():
    recognition = Recognition()
    if(recognition.eyeTrack()):
        userId = str(recognition.FaceRecognition())
        response['face'] = userId
        return list(db.users.find({'user_id' : userId },{'_id' : 0}))
        
def arduinoSerialRead(entryId):
    print(entryId)
    while  True:
        data = serial.readline().decode('UTF-8')
        if(data!=''):
            if('response-finger' in data):
                if('finger' in response):
                    continue
                response['finger'] = (data.split('-')[1]).split('=')[1]
            if('response-card' in data):
                if('card' in response):
                    continue
                response['card'] = (data.split('-')[1]).split('=')[1]
        print(response)




def startArduinoRecognition():
    serial.write('9'.encode())


@eel.expose
def recognition(entryId):
    Thread(target = arduinoSerialRead, args = (entryId,)).start()
    faceRecognition()
    startArduinoRecognition()



eel.start('user/login.html')




 

