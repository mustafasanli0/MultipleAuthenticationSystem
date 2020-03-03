from cv2 import *
userImagePath = os.path.abspath(os.getcwd())+'/Panel/user/images/'


def takePhoto(username):

    cam = cv2.VideoCapture(2)
    while True:
        ret_val, img = cam.read()
        cv2.imshow('Take A Photo', img)
        keyboard=cv2.waitKey(1)
        
        if keyboard == ord('s'):
            imwrite(userImagePath+username+".jpg",img)
            cv2.destroyAllWindows()
            return username+".jpg"
        elif keyboard == ord('q'):
            cv2.destroyAllWindows()
            break