import os
import sys
import numpy as np
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
        results = self.model.predict(frame, verbose=False, conf=self.pred_thresh, classes=self.get_class_number(objects=self.obj), 
                                     imgsz=704, device=self.device)
        return results
    
    #Get the center of each bbox detected
    def get_box_center_coor(self, results):
        for r in results:
            centers = [(int(x.item()),int(y.item())) for (x,y,_,_) in(r.boxes.xywh)]
        return centers
    
    #Get the corners of each bbox detected
    def get_box_coor(self, results):
        for r in results:
            corners = [(int(x1.item()),int(y1.item()), int(x2.item()), int(y2.item())) for (x1,y1,x2,y2) in(r.boxes.xyxy)]
        return corners
    
    def draw_center_point(self, image, centers):
        image_frame = np.copy(image)
        for center_coord in centers:
            cv2.circle(image_frame, center_coord, 4, (0,0,255), -1)
        return image_frame

#Image analyzing and heatmap generator: each time a detection is made, sums 1 to a matrix that records object positions
class Heatmap_analyzer():
    def __init__(self, width, height, alpha=0.7):
        self.width = width
        self.height = height
        self.alpha = alpha
        self.heatmap_matrix = np.zeros((height, width, 3), dtype=np.float32)
    
    #Only considers the bbox center as object position
    def process_centers(self, centers):
        for center in centers:
            self.heatmap_matrix[center[1], center[0]] += 1
    
    #Considers full bbox as object position
    def process_bbox(self, xyxy):
        for xyxy_coor in xyxy:
            self.heatmap_matrix[xyxy_coor[1]:xyxy_coor[3], xyxy_coor[0]:xyxy_coor[2]] += 1
        
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
    video_path = r'.\videos\Mall.mp4'
    model_path = r'models\yolov8m.pt'
    
    #Video capture and information
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) #10

    #Objects initialization 
    detector = Detector(model_path, obj='person')
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

        #Process each frame
        processed_frame = result[0].plot(probs=False, labels=False, boxes=False)
        
        centers = detector.get_box_center_coor(result) #Get bboxes center
        centers_drawn = detector.draw_center_point(processed_frame, centers)

        xyxy = detector.get_box_coor(result) #Get bboxes corner

        #Heatmap_analysis
        #heatmap_frame = heatmap.process_centers(centers) #Only considers the bbox center as object position
        heatmap_frame = heatmap.process_bbox(xyxy) #Considers full bbox as object position

        #Show detections        
        #cv2.imshow('Processed_frame', centers_drawn)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Get the final frame (only for showing purposes)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    _, last_frame = cap.read()

    heatmap.show_and_save(last_frame, name='heatmap_mall')

    cap.release()
    cv2.destroyAllWindows()