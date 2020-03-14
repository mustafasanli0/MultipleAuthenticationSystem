import face_recognition
import cv2
import numpy as np
from .gaze_tracking import GazeTracking
from App.MongoDBConnection import db
import os, json

class Recognition:

    def __init__(self):
        self.video_capture = cv2.VideoCapture(2)
        self.blinkDetectNum=10
        self.running=True

    def eyeTrack(self):

        gaze = GazeTracking()
        blinkCount=0

        while True:

                # Grab a single frame of video
                ret, frame = self.video_capture.read()

                # We send this frame to GazeTracking to analyze it
                gaze.refresh(frame)

                frame = gaze.annotated_frame()
                text = ""


                if gaze.is_blinking():
                    text = "Goz Kirpildi"
                    blinkCount+=1
                elif gaze.is_right():
                    text = "Saga Bakildi"
                elif gaze.is_left():
                    text = "Sola Bakildi"
                elif gaze.is_center():
                    text = "Merkeze Bakildi"
                

                cv2.putText(frame, text, (0, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (147, 58, 31), 2)
                
                # Display the resulting image
                cv2.imshow('Video', frame)
                print("Goz Kırpma: "+str(blinkCount))

                if not self.running:
                    # Release handle to the webcam
                    self.video_capture.release()
                    cv2.destroyAllWindows()
                    return 0

                if blinkCount>=self.blinkDetectNum:
                    return 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    def stop(self):
        self.running = False
        
    def getAllUsers(self):
        return  db.users.find({},{'_id':0})
    
    def FaceRecognition(self):
        prevPath = os.path.abspath(os.getcwd())
        userImagePath=prevPath+"/Panel/user/images/"

         # Create arrays of known face encodings and their names
        known_face_encodings = []
        known_face_names = []

        users = list(self.getAllUsers())
        for document in users:
            if document['user_id']== '0':
                continue
            user_id = document['user_id']
            photo = face_recognition.face_encodings(face_recognition.load_image_file(userImagePath+document['photo']))[0]
            known_face_names.append(user_id)
            known_face_encodings.append(photo)

       


       

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        
        ret, frame = self.video_capture.read()
        
        
        while True: #default TRUE
            
            if not self.running:
                return 0
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:

                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Bilinmiyor"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
                    
            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Release handle to the webcam
                self.video_capture.release()
                cv2.destroyAllWindows()

                if len(face_locations)>1:
                    return 11 

                return name
                
            
            
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        
