from cv2 import *

def takePhoto(username):

    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        cv2.imshow('my webcam', img)
        keyboard=cv2.waitKey(1)
        
        if keyboard == ord('s'):
            imwrite(username+".jpg",img)
            return username+'.jpg'
        elif keyboard == ord('q'):
            break
        
    cv2.destroyAllWindows()