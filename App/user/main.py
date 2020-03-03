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

def getVerificationOption(userId,entryId):
    accessible = db.users.find_one({'user_id' : userId },{'_id' : 0})['accessible']
    if(entryId in accessible):
        return accessible[entryId]
    else:
        return 'ACCESS_DENIED'
    

@eel.expose
def getEntries():
    entries = db.entries.aggregate([
    {"$project": {"_id": { "$toString": "$_id" }, 'entry':1 } }
    ])
    return list(entries)


response = {}
verification = ["FULL"]
accessUserId = '0'
def faceRecognition(entryId):
    global accessUserId
    recognition = Recognition()
    if(recognition.eyeTrack()):
        userId = str(recognition.FaceRecognition())
        response['face'] = userId
        

        if('FULL' in verification):
            verification.remove('FULL')
            getVerification = getVerificationOption(userId, entryId)
            if(getVerification == "ACCESS_DENIED"):
                print("ACCESS DENIED")
                return 'ACCESS_DENIED'
            verification.append(getVerification)
            accessUserId = userId
            try:
                verification[0].remove('face')
            except ValueError:
                pass
        else:
            if(accessUserId == userId):
                try:
                    verification[0].remove('face')
                except ValueError:
                        pass
            else:
                print("ACCESS DENIED")
                return 'ACCESS_DENIED'

            
        return list(db.users.find({'user_id' : userId },{'_id' : 0}))
        
def arduinoSerialRead(entryId):
    global accessUserId
    while  True:
        data = serial.readline().decode('UTF-8')
        if(data!=''):
            if('response-finger' in data):
                if('finger' in response):
                    continue
                response['finger'] = (data.split('-')[1]).split('=')[1] # Userid

                if('FULL' in verification):
                    verification.remove('FULL')
                    getVerification = getVerificationOption(response['finger'], entryId)
                    if(getVerification == "ACCESS_DENIED"):
                        print("ACCESS DENIED")
                        return 'ACCESS_DENIED'
                    verification.append(getVerification)
                    accessUserId = response['finger']
                    try:
                        verification[0].remove('finger')
                    except ValueError:
                        pass
                else:
                    if(accessUserId == response['finger']):
                        try:
                            verification[0].remove('finger')
                        except ValueError:
                            pass
                    else:
                        print("ACCESS DENIED")
                        return 'ACCESS_DENIED'
            if('response-card' in data):
                if('card' in response):
                    continue
                response['card'] = (data.split('-')[1]).split('=')[1] # Userid

                if('FULL' in verification):
                    verification.remove('FULL')
                    getVerification = getVerificationOption(response['card'], entryId)
                    if(getVerification == "ACCESS_DENIED"):
                        print("ACCESS DENIED")
                        return 'ACCESS_DENIED'
                    verification.append(getVerification)
                    accessUserId = response['card']
                    try:
                        verification[0].remove('card')
                    except ValueError:
                        pass
                else:
                    if(accessUserId == response['card']):
                        try:
                            verification[0].remove('card')
                        except ValueError:
                            pass
                    else:
                        print("ACCESS DENIED")
                        return 'ACCESS_DENIED'
        print(verification)
        if(verification==[[]]):
            print("ACCESS GRANTED!:",accessUserId)




def startArduinoRecognition():
    serial.write('9'.encode())


@eel.expose
def recognition(entryId):
   
    t=Thread(target = arduinoSerialRead, args = (entryId,))
    t.start()
    startArduinoRecognition()
    faceRecognition(entryId)    



eel.start('user/login.html')




 

