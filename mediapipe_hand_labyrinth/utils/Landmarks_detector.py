import numpy as np
import matplotlib.pyplot as plt
import cv2
import mediapipe as mp
import math
import time

class LandmarkDetector():

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils #Draw the interconected lines
        self.mp_holistic = mp.solutions.holistic #Hand tracking on real time - Hands detection model
        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    def get_positions(self, image, kind='pose', draw=True):
        
        self.landmarks_list = []
        results = self.holistic.process(image)
        
        if kind=='left_hand' and results.left_hand_landmarks:
            landmarks = results.left_hand_landmarks.landmark
            if draw:
                self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                               landmark_drawing_spec = self.mp_drawing.DrawingSpec(color=(255,0,0), thickness=cv2.FILLED, circle_radius=4),
                                               connection_drawing_spec = self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1))
                

        elif kind=='right_hand' and results.right_hand_landmarks:
            landmarks = results.right_hand_landmarks.landmark
            if draw:
                self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                      landmark_drawing_spec = self.mp_drawing.DrawingSpec(color=(255,0,0), thickness=cv2.FILLED, circle_radius=4),
                                      connection_drawing_spec = self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=1))


        elif kind=='face' and results.face_landmarks:
            landmarks = results.face_landmarks.landmark
            if draw:
                self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_TESSELATION,
                                               landmark_drawing_spec = self.mp_drawing.DrawingSpec(color=(255,0,0), thickness=cv2.FILLED, circle_radius=2),
                                               connection_drawing_spec = self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1))

        elif kind=='pose' and results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            if draw:
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
                                               landmark_drawing_spec = self.mp_drawing.DrawingSpec(color=(255,0,0), thickness=cv2.FILLED, circle_radius=2),
                                               connection_drawing_spec = self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=1))
        
        else:
            detection = False
            landmarks = False
            #print("No landmarks detected")                    

        if landmarks:  
            detection = True 
            for id, lm in enumerate(landmarks):
                center_x, center_y = int(lm.x * image.shape[1]), int(lm.y * image.shape[0])
                self.landmarks_list.append([id, center_x, center_y])
    
        return detection, self.landmarks_list

    #Get positions of only one landmark
    def filter_landmark(self, landmarks_list, idx=None):
        return landmarks_list[idx][1:]

    #get distance between two points
    def get_distance(self, point_1, point_2):
        #point.shape = [x,y]
        return math.sqrt(abs(point_1[0] - point_2[0])**2 + abs(point_1[1] - point_2[1]))
    

def main():
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) #3 -> Width of the frames in the video stream
    cap.set(4, 720) #4 ->Height of the frames in the video stream
    cap.set(5, 30) #5 -> 30 FPS

    detector = LandmarkDetector()

    while cap.isOpened():  

        # Capture the video frame by frame
        ret, frame = cap.read()

        #Flip the image to see in selfie style
        #image = cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #Detections: results.pose_landmarks - results.face_landmarks - results.left_hand_landmarks, results.right_hand_landmarks
        #right_det, right_detections_list = detector.get_landmarks(image, kind='right_hand', draw=False)
        left_det, left_detections_list = detector.get_positions(image, kind='left_hand', draw=True)
        #face_det, face_detections_list = detector.get_positions(image, kind='face', draw=True)

        #if right_det:
        #    right_landmark = detector.filter_landmark(right_detections_list, idx=8)
        #    cv2.circle(image, center=right_landmark, radius=10, color=(255,0,0), thickness=cv2.FILLED)

        #if left_det:
        #    left_landmark = detector.filter_landmark(left_detections_list, idx=8)
        #    cv2.circle(image, center=left_landmark, radius=10, color=(255,0,0), thickness=cv2.FILLED)

        #if face_det:
        #    face_landmark = detector.filter_landmark(face_detections_list, idx=8)
        #    cv2.circle(image, center=face_landmark, radius=10, color=(255,0,0), thickness=cv2.FILLED)
        
        if left_det:
            #Get points' distance
            finger_tip = detector.filter_landmark(left_detections_list, idx=8)
            mayor_tip = detector.filter_landmark(left_detections_list, idx=12)
            cv2.circle(image, center=finger_tip, radius=10, color=(255,0,0), thickness=cv2.FILLED)
            cv2.circle(image, center=mayor_tip, radius=10, color=(255,0,0), thickness=cv2.FILLED)
            distance = detector.get_distance(finger_tip, mayor_tip)
            #Put text
            #cv2.putText(image, str(f'Distance: {distance}'), (10,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

        #Recolor image back to BGR for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
       
        # Display the resulting frame
        image = cv2.flip(image,1)

        if left_det:
            cv2.putText(image, str(f'Distance: {distance}'), (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

        cv2.imshow('Landmark Detector', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()