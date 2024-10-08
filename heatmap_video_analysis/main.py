import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
import torch
from ultralytics import YOLO

class Detector():
    def __init__(self, model_path, obj='person'):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.load_YOLO_model(model_path)
        self.pred_thresh = 0.5
        self.classes = list(self.model.model.names.values())
        self.obj = [obj]

    def load_YOLO_model(self, model_path):
        model = YOLO(model_path)
        return model

    def get_class_number(self, objects=None):
        number_class_list = []
        if objects!=None:
            if objects!=['all']:
                for object in objects: 
                    number_class_list.append(self.classes.index(object))
            elif objects == ['all']:
                number_class_list = list(range(len(self.classes)))
        
        return number_class_list

    def predict(self, frame):
        results = self.model.predict(frame, verbose=False, conf=self.pred_thresh, classes=self.get_class_number(objects=self.obj), 
                                     imgsz=704, device=self.device)
        return results
    
    def get_box_center_coor(self, results):
        for r in results:
            centers = [(int(x.item()),int(y.item())) for (x,y,_,_) in(r.boxes.xywh)]
        return centers
    
    def draw_center_point(self, image, centers):
        image_frame = np.copy(image)
        for center_coord in centers:
            cv2.circle(image_frame, center_coord, 4, (0,0,255), -1)
        return image_frame


class Heatmap_analyzer():
    def __init__(self, width, height, frames_to_save=200, alpha=0.7, colormap='jet'):
        self.width = width
        self.height = height
        self.frames_to_save = frames_to_save
        self.alpha = alpha
        self.colormap = colormap
        self.heatmap_matrix = np.zeros((width, height, 3), dtype=np.float32)
    
    def process(self, frame, centers):
        pass


if __name__ == '__main__':

    if not os.path.exists(r'.\models'):
        os.makedirs(r'.\models')

    if not os.path.exists(r'.\outputs'):
        os.makedirs(r'.\outputs')

    video_path = r'.\videos\people.mp4'
    model_path = r'models\yolov8m.pt'
    #model_path = r'models\yolo11m.pt'
    
    #Objects initialization 
    detector = Detector(model_path, obj='car')

    cap = cv2.VideoCapture(video_path)
    cap.set(3, 1280) #3 -> Width of the frames in the video stream
    cap.set(4, 720)

    # Codec and VideoWriter
    codec = cv2.VideoWriter_fourcc(*'MP4V')
    fps = cap.get(cv2.CAP_PROP_FPS) #10
    #delay = int(500 / fps)  # delay between frames per miliseconds
    #video_writer = cv2.VideoWriter(r'.\outputs\output_fail.mp4', codec, fps, (1280,720))

    while cap.isOpened():
        
        #Import image from camera
        ret, frame = cap.read()
        if not ret:
            print("Video frame is empty or video processing has been successfully completed.")
            break

        #Get predictions  
        result = detector.predict(frame)
        
        #Process each frame
        processed_frame = result[0].plot(probs=False, labels=False, boxes=False)
        centers = detector.get_box_center_coor(result) #Get bboxes center
        centers_frame = detector.draw_center_point(processed_frame, centers)

        #Show results        
        cv2.imshow('processed_frame', centers_frame)

        # Press 'q' to exit the loop
        #if cv2.waitKey(delay) & 0xFF == ord('q'):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    #video_writer.release()
    cv2.destroyAllWindows()