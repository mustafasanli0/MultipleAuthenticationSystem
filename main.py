from FaceRecognition import Recognition
import gaze_tracking
import eel
eel.init('Panel')

@eel.expose
def faceRecognition():
    recognition = Recognition()
    if(recognition.eyeTrack()):
        return recognition.FaceRecognition()

eel.start('pages/examples/login.html')




 

