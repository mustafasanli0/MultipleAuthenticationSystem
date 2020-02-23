import sys,os,time
prevPath = os.path.abspath(os.getcwd())
sys.path.insert(0,prevPath)
import jwt
from Modules.FaceRecognition import Recognition
import Modules.gaze_tracking
from App.MongoDBConnection import db
import eel
eel.init('Panel')


@eel.expose
def login(a,b):
    user = 1
    
    if user is not None :
        jwt_encode = jwt.encode({'user': {'username':'msanli14','name':'Mustafa','surname':'Sanlı','phone':'05457120478'}}, 'Hacklemigelkeklemi', algorithm='HS256')
        return str(jwt_encode)
    else:
        return "error"
    
@eel.expose
def showDashboard():
    os.system('python3 '+os.path.abspath(os.getcwd())+'/App/admin/dashboard.py')






eel.start('admin/login.html')






 

