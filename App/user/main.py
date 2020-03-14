import sys,os,time
prevPath = os.path.abspath(os.getcwd())
sys.path.insert(0,prevPath)

from Modules.FaceRecognition import Recognition
import Modules.gaze_tracking
from App.MongoDBConnection import db
import eel
from threading import Thread
import serial

def startArduinoRecognition():
    serial.write('9'.encode())

serial = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
time.sleep(2)
startArduinoRecognition()
eel.init('Panel')

def getVerificationOption(userId,entryId):
    accessible = db.users.find_one({'user_id' : userId },{'_id' : 0})['accessible']
    if(entryId in accessible):
        return accessible[entryId]
    else:
        eel.getAccessDenied()
        return 'ACCESS_DENIED'
    

@eel.expose
def getEntries():
    entries = db.entries.aggregate([
    {"$project": {"_id": { "$toString": "$_id" }, 'entry':1 } }
    ])
    return list(entries)


response = {}
verification = ["FULL"]
accessUserId = '-1'
recognitionClass = Recognition()
def faceRecognition(entryId):
    global accessUserId
    global recognitionClass
    if(recognitionClass.eyeTrack()):
        userId = str(recognitionClass.FaceRecognition())
        response['face'] = userId
        

        if('FULL' in verification):
            verification.remove('FULL')
            getVerification = getVerificationOption(userId, entryId)
            if(getVerification == "ACCESS_DENIED"):
                print("ACCESS DENIED")
                recognitionClass.stop()
                eel.getAccessDenied()
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
                recognitionClass.stop()
                eel.getAccessDenied()
                return 'ACCESS_DENIED'

            
        return list(db.users.find({'user_id' : userId },{'_id' : 0}))

def arduinoSerialRead(entryId):
    global accessUserId
    global recognitionClass
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
                        recognitionClass.stop()
                        eel.getAccessDenied()
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
                        recognitionClass.stop()
                        eel.getAccessDenied()
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
                        recognitionClass.stop()
                        eel.getAccessDenied()
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
                        recognitionClass.stop()
                        eel.getAccessDenied()
                        return 'ACCESS_DENIED'
        userResp, verificationResp = getUserAndVerification(accessUserId, verification)
        eel.getUserResponse(userResp, verificationResp)

        if(verification==[[]]):
            print("ACCESS GRANTED!:",accessUserId)
            recognitionClass.stop()
            return 1
            


def getUserAndVerification(userId=-1,verification=0):
    return db.users.find_one({'user_id' : userId },{'_id' : 0}), verification





@eel.expose
def recognition(entryId):
    arduinoThread = Thread(target = arduinoSerialRead, args = (entryId,))
    arduinoThread.start()
    faceRecognition(entryId)
    

eel.start('user/login.html')




 

