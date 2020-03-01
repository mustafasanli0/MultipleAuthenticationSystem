import sys,os,time
import hashlib
prevPath = os.path.abspath(os.getcwd())
sys.path.insert(0,prevPath)
import jwt
from Modules.FaceRecognition import Recognition
import Modules.gaze_tracking
from App.MongoDBConnection import db
import eel
eel.init('Panel')


@eel.expose
def login(username_,password_):
    password = hashlib.md5(password_.encode()).hexdigest()

    admin = db.users.find_one({'username':str(username_),'password':str(password),'role':'1'},{'password':0,'_id':0})
    
    if admin is not None :
        jwt_encode = jwt.encode(admin, 'Hacklemigelkeklemi', algorithm='HS256')
        return str(jwt_encode)
    else:
        return "error"
    
@eel.expose
def showDashboard():
    os.system('python3 '+os.path.abspath(os.getcwd())+'/App/admin/dashboard.py')






eel.start('admin/login.html')






 

