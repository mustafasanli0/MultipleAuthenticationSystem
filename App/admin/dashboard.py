import sys,os,time
prevPath = os.path.abspath(os.getcwd())
sys.path.insert(0,prevPath)
import jwt
from Modules.FaceRecognition import Recognition
import Modules.gaze_tracking
from Modules.Photo import takePhoto
from App.MongoDBConnection import db
import eel
eel.init('Panel')


@eel.expose
def jwtDecode(cookie):
    jwtSplit = cookie.split('=')[1]
    jwtSplit = (jwtSplit[2:]).replace('\'','')
    jwtResp = jwt.decode(jwtSplit, 'Hacklemigelkeklemi', algorithms=['HS256'])
    return jwtResp

@eel.expose
def setPhoto(userId):
    return takePhoto(userId)

eel.start('admin/dashboard.html',port=8001)
