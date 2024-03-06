import cv2
import torch
import keyboard
from ultralytics import YOLO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

########################### EMAIL SENDER CONFIGURATION ##########################
from email_settings import *
# Open: https://myaccount.google.com/apppasswords, generate an App name and copy the generated password, after that you should complete the next variables
password = password
from_email = from_email  # must match the email used to generate the password
to_email = to_email  # receiver email

# Server configuration
server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
server.login(from_email, password)
#################################################################################


class Security_system():
    def __init__(self, model_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.email_sent = False
        self.start_recording = False
        self.model = self.load_YOLO_model(model_path)
        self.classes = list(self.model.model.names.values())
        self.pred_thresh = 0.5
        self.class_detect = ['person']

    def get_class_number(self, objects=None):
        number_class_list = []
        if objects!=None:
            if objects!=['all']:
                for object in objects: 
                    number_class_list.append(self.classes.index(object))
            elif objects == ['all']:
                number_class_list = list(range(len(self.classes)))
        
        return number_class_list

    def load_YOLO_model(self, model_path):
        model = YOLO(model_path)
        return model

    def predict(self, frame):
        results = self.model.predict(frame, verbose=False, conf=self.pred_thresh, classes=self.get_class_number(objects=self.class_detect), imgsz=704, device=self.device)
        return results

    def send_email(self, to_email, from_email, object_name, object_detected=1):
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = "Security Camera Alert"
        # Add in the message body
        message_body = f'ALERT - {object_detected} {object_name} has been detected!! \nThe video recording will start now'
        message.attach(MIMEText(message_body, 'plain'))
        server.sendmail(from_email, to_email, message.as_string())
    
    def control(self, results, video_writer):
        detected_class = results[0].boxes.cls
        #print(f"{len(detected_class)} Person detected")
        if len(detected_class) > 0:
            if not self.email_sent:
                self.send_email(to_email, from_email, self.class_detect[0], object_detected=len(detected_class))
                self.email_sent = True
                print("Email sent, staring recording video...")
            self.start_recording = True
        else:
            #self.email_sent = False #Only sent email for the first detection
            self.start_recording = False
            print("Video recording stopped")
        
        #Recording video
        if self.start_recording:
            print("Recording....")
            annotated_frame = results[0].plot()
            video_writer.write(annotated_frame)
        

if __name__ == "__main__":

    model_path = r'models/yolov8m.pt'
    system = Security_system(model_path)
    
    #Video Configuration
    cap = cv2.VideoCapture(0) # or "path/to/video/file.mp4"
    video_size = (1280, 720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, video_size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, video_size[1])
    # Codec and VideoWriter
    codec = cv2.VideoWriter_fourcc(*'MP4V')
    fps = cap.get(cv2.CAP_PROP_FPS) #10
    video_writer = cv2.VideoWriter(r'.\outputs\camera_system.mp4', codec, fps, video_size)

    def check_key_pressed(key):
        return keyboard.is_pressed(key)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        
        results = system.predict(frame)
        system.control(results, video_writer)
        
        if check_key_pressed('q'):
            print("Saving video recording if exists...")
            break

cap.release()
video_writer.release()
cv2.destroyAllWindows()
server.quit()