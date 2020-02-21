import sys,os
prevPath = os.path.abspath(os.getcwd())
sys.path.insert(0,prevPath)

from Modules.FaceRecognition import Recognition
import Modules.gaze_tracking
from App.MongoDBConnection import db
import eel
eel.init('Panel')


@eel.expose
def faceRecognition():
    recognition = Recognition()
    if(recognition.eyeTrack()):
        return recognition.FaceRecognition()

eel.start('user/login.html')




 

