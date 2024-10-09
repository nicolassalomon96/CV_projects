import os
import sys
import numpy as np
import math
from collections import defaultdict
import matplotlib.pyplot as plt
import cv2
import torch
from ultralytics import YOLO

#Object Detector Class
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
        results = self.model.track(frame, persist=True, classes=self.get_class_number(objects=self.obj), device=self.device, verbose=False)
        return results

    def get_boxes_and_track_id(self, results):
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        return zip(boxes, track_ids)
    
#Image analyzing and heatmap generator: each time a detection is made, sums 1 to a matrix that records object positions
class Heatmap_analyzer():
    def __init__(self, width, height, alpha=0.7):
        self.width = width
        self.height = height
        self.alpha = alpha
        self.heatmap_matrix = np.zeros((height, width, 3), dtype=np.float32)
        self.track_history = defaultdict(lambda: [])
        self.last_positions = {}
        
    #Considers full bbox as object position
    def process_bbox(self, boxes_with_id):
        for box, track_id in boxes_with_id:
            x_center, y_center, width, height = box
            current_position = (float(x_center), float(y_center))

            top_left_x = max(0, int(x_center - width / 2))
            top_left_y = max(0, int(y_center - height / 2))
            bottom_right_x = min(self.heatmap_matrix.shape[1], int(x_center + width / 2))
            bottom_right_y = min(self.heatmap_matrix.shape[0], int(y_center + height / 2))

            track = self.track_history[track_id]
            track.append(current_position)
            if len(track) > 1200:
                track.pop(0)
        
            last_position = self.last_positions.get(track_id)
            if last_position and self.calculate_distance(last_position, current_position) > 5:
                self.heatmap_matrix[top_left_y:bottom_right_y, top_left_x:bottom_right_x] += 1

            self.last_positions[track_id] = current_position

    
    def calculate_distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        
    def show_and_save(self, last_frame, name='example'):
        heatmap_blurred = cv2.GaussianBlur(self.heatmap_matrix, (15, 15), 0)
        heatmap_norm = cv2.normalize(heatmap_blurred, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        heatmap_color = cv2.applyColorMap(heatmap_norm, cv2.COLORMAP_JET)
        overlay = cv2.addWeighted(last_frame, 1 - self.alpha, heatmap_color, self.alpha, 0)
    
        cv2.imshow('Heatmap', overlay)
        cv2.waitKey(0)
        cv2.imwrite(rf'outputs\{name}.png', overlay)


if __name__ == '__main__':

    if not os.path.exists(r'.\models'):
        os.makedirs(r'.\models')

    if not os.path.exists(r'.\outputs'):
        os.makedirs(r'.\outputs')

    #video_path = r'.\videos\people_loop.mp4'
    #video_path = r'.\videos\CCTV.mp4'
    #video_path = r'.\videos\Mall.mp4'
    video_path = r'.\videos\road.mp4'
    #model_path = r'models\yolov8m.pt'
    model_path = r'models\yolov10m.pt'
    
    #Video capture and information
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) #10

    #Objects initialization 
    detector = Detector(model_path, obj='car')
    heatmap = Heatmap_analyzer(width=width, height=height)

    #Processing Loop
    print("Processing video... This may take some minutes")
    while cap.isOpened():
        
        #Import image from camera
        ret, frame = cap.read()
        if not ret:
            print("Video frame is empty or video processing has been successfully completed.")
            break

        #Get predictions  
        result = detector.predict(frame)
        boxes_with_id = detector.get_boxes_and_track_id(result)

        #Process each frame
        processed_frame = result[0].plot()
        cv2.imshow("Tracking", processed_frame)
               
        #Heatmap_analysis
        heatmap_frame = heatmap.process_bbox(boxes_with_id) #Considers full bbox as object position
   

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Get the final frame (only for showing purposes)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    _, last_frame = cap.read()

    heatmap.show_and_save(last_frame, name='heatmap_road_dynamic')

    cap.release()
    cv2.destroyAllWindows()