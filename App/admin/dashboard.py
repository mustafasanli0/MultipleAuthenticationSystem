import sys,os,time
prevPath = os.path.abspath(os.getcwd())
sys.path.insert(0,prevPath)
import jwt, json
from Modules.FaceRecognition import Recognition
import Modules.gaze_tracking
from Modules.Photo import takePhoto
from App.MongoDBConnection import db
import serial
from threading import Thread
import eel
eel.init('Panel')
serial = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)


@eel.expose
def getEntries():
    entries = db.entries.aggregate([
    {"$project": {"_id": { "$toString": "$_id" }, 'entry':1 } }
    ])
    return list(entries)


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


def splitAuthorization(form):
    data={}
    for key, value in form.items():
        if value == 'on' or ':' in value:
            keyArr = key.split('-')
            if(len(keyArr) == 1):
                data[key]=[]
                data[keyArr[0]].append({'verification':[]})
            else:
               
                if(keyArr[1] == 'start'):
                    data[keyArr[0]].append({'start':value})
                elif(keyArr[1] == 'end'):
                    data[keyArr[0]].append({'end':value})
                else:
                    data[keyArr[0]][0]['verification'].append(keyArr[1])
    return data

@eel.expose
def setUserForm(userdata):
    form = json.loads(json.dumps(userdata))
    data = []
    auth = splitAuthorization(form)
    data.append({'user_id':form['user_id'], 
    'username':form['username'], 
    'name':form['name'],
    'surname':form['surname'],
    'phone':form['phone'],
    'photo':form['photo_name'],
    'accessible':auth})
    db.users.insert_many(data)

    


@eel.expose
def getLastUserId():
    user = db.users.find().sort("user_id",-1).limit(1)
    return (int(list(user)[0]['user_id'])+1)



            



serialReadThread = Thread(target = arduinoSerialRead, args = ())
@eel.expose
def startSerialRead():
    serialReadThread.start()




eel.start('admin/dashboard.html',port=8001)

