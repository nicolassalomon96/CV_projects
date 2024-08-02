#Import libraries
import os
import numpy as np
import cv2
import mediapipe as mp
import face_recognition as fr
import tkinter as tk
from tkinter import font
import imutils
import math
from PIL import Image, ImageTk
from datetime import datetime

############################################### PAHTS ###########################################################
database_folder = r'.\Database'
users_folder = r'.\Database\Users'
faces_folder = r'.\Database\Faces'
images_folder = r'.\Images'
reg_folder = r'.\Database\Registrations'

if not os.path.exists(database_folder):
    os.mkdir(database_folder)

if not os.path.exists(users_folder):
    os.mkdir(users_folder)

if not os.path.exists(faces_folder):
    os.mkdir(faces_folder)

if not os.path.exists(reg_folder):
    os.mkdir(reg_folder)

############################################# VARIABLES #########################################################
show_det = False #Show face mesh image
blink = False
blink_count = 0
step = 1
info = [] #Records information about the user

padx = 20 #Offset used when capturing the face through the camera
pady = 80
recog_thres = 0.5 #Recognition Threshold

############################################### FUNCTIONS #######################################################
def get_day_and_hour():
    current_time = datetime.now()
    day = current_time.strftime("%A")
    time = current_time.strftime("%d/%m/%Y %H:%M:%S")
    return day, time

def close_window_2():
    global step, blink_count
    step = 1
    blink_count = 0
    screen_2.destroy()

def close_window_4():
    global step, blink_count
    step = 1
    blink_count = 0
    screen_4.destroy()

# Show the profile when face is detected  
def Profile(username):
    global step, blink_count, users, users_folder, face_images, screen_4

    #Reset Variables
    step = 0
    blink_count = 0

    screen_4 = tk.Toplevel(screen)
    screen_4.title('Profile')
    screen_4.geometry('1280x720')
    #Set background
    background_4 = tk.Label(screen_4, image = back_image_4, text='Start')
    background_4.place(x=0, y=0, relheight=1, relwidth=1)

    #Read user file
    with open(f'{os.path.join(users_folder, username)}.txt', 'r') as f:
        InfoUser = f.read().split(',')

    Name = InfoUser[0]
    User = InfoUser[1]
    
    # Check
    if User in users:
        # Interface
        text1 = tk.Label(screen_4, text=f"Name: {Name}")
        text1.config(font='Helvetica 18 bold')
        text1.place(x=340, y=560)

        text2 = tk.Label(screen_4, text=f"Username: {User}")
        text2.config(font='Helvetica 18 bold')
        text2.place(x=320, y=595)
        
        # Label
        lblImgUser = tk.Label(screen_4)
        lblImgUser.place(x=250, y=150)

        # User Image
        PosUserImg = users.index(User)
        UserImg = face_images[PosUserImg]

        ImgUser = Image.fromarray(UserImg)
        
        ImgUser = cv2.imread(f'{os.path.join(faces_folder, User)}.png')
        ImgUser = cv2.cvtColor(ImgUser, cv2.COLOR_RGB2BGR)
        ImgUser = Image.fromarray(ImgUser)
        
        IMG = ImageTk.PhotoImage(image=ImgUser)

        lblImgUser.configure(image=IMG)
        lblImgUser.image = IMG

        #Create or add registraion date file
        day, time = get_day_and_hour()
        filename = Name + '_' + User + r'.txt'
        with open(f'{os.path.join(reg_folder, filename)}', 'a+') as f:
            f.write(f'Name: {Name} - User: {User} - Datetime: {day} - {time}\n')
    
    screen_4.protocol("WM_DELETE_WINDOW", close_window_4)

# Code Faces function
def Code_Faces(images):
    code_faces_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cod_img = fr.face_encodings(img)[0]
        code_faces_list.append(cod_img)   
    return code_faces_list

# Get face image and face landmarks for biometric log
def Biometric_Log():
    global screen_2, show,det, blink_count, blink, step, video_label, padx, pady, user_reg

    if cap is not None:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=1280, height=720)
     
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret == True:
            res_face = FaceMesh.process(frame_rgb)

            #Result list
            px = []
            py =[]
            points_list = []
            if res_face.multi_face_landmarks: #Detections made?
                for faces in res_face.multi_face_landmarks:
                    if show_det:
                        mpDraw.draw_landmarks(frame, faces, FaceMeshObj.FACEMESH_CONTOURS, ConfigDraw, ConfigDraw)
                    
                    #Get face points info
                    for id, points in enumerate(faces.landmark):

                        h, w, c = frame.shape
                        x, y = int(points.x * w), int(points.y * h) #Points in frame coordinates
                        px.append(x)
                        py.append(y)
                        points_list.append([id, x, y])
                    
                        if len(points_list) == 468: #Mediapipe gives you 468 Keypoints
                            #Right Eye Points
                            x1, y1 = points_list[145][1:] #Up point
                            x2, y2 = points_list[159][1:] #Down point
                            distance_right_eye_points = math.hypot(x2-x1, y2-y1)

                            #Left Eye Points
                            x3, y3 = points_list[374][1:] #Up point
                            x4, y4 = points_list[386][1:] #Down point
                            distance_left_eye_points = math.hypot(x4-x3, y4-y3)

                            #Right Temple Points
                            x5, y5 = points_list[139][1:] #Up point

                            #Left Temple Points
                            x6, y6 = points_list[368][1:] #Up point

                            #Right Eyebrow
                            x7, y7 = points_list[70][1:] #Up point

                            #Left Eyebrow
                            x8, y8 = points_list[300][1:] #Up point

                            #Face detection
                            faces = face_detector.process(frame_rgb)
                            if faces.detections is not None:
                                for face in faces.detections:
                                    score = face.score[0]
                                    bbox = face.location_data.relative_bounding_box
                                    if score > recog_thres:
                                        #Bbox to pixels coordinates
                                        bbox_x1, bbox_y1, bbox_w, bbox_h = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)

                                        #apply padding
                                        offset_w = (padx/100)*bbox_w
                                        bbox_x1 = int(bbox_x1 - offset_w/2) if int(bbox_x1 - offset_w/2) > 0 else 0
                                        bbox_w = int(bbox_w + offset_w) if int(bbox_w + offset_w) > 0 else 0
                                        offset_h = (pady/100)*bbox_h
                                        bbox_y1 = int(bbox_y1 - offset_h/2) if int(bbox_y1 - offset_h/2) > 0 else 0
                                        bbox_h = int(bbox_h + offset_h/2) if int(bbox_h + offset_h/2) > 0 else 0

                                        if step == 1:
                                            #Draw rectangle
                                            cv2.rectangle(frame, (bbox_x1, bbox_y1, bbox_w, bbox_h), (255,0,0), 2)

                                            #Show Step_1 image
                                            h1, w1, _ = img_step1.shape
                                            frame_cp = np.copy(frame)
                                            frame[20:20+h1, 345:345+w1] = img_step1

                                            if x7 > x5 and x8 < x6:
                                                #The person is looking at the camera
                                                frame = frame_cp
                                                cv2.rectangle(frame, (bbox_x1, bbox_y1, bbox_w, bbox_h), (0,255,0), 2)

                                                #Show Step_11 image
                                                h11, w11, _ = img_step11.shape
                                                frame_cp = np.copy(frame)
                                                frame[20:20+h11, 345:345+w11] = img_step11

                                                #blinking counter
                                                if distance_right_eye_points <= 10 and distance_left_eye_points <= 10 and blink == False:
                                                    blink_count += 1
                                                    blink = True
                                                elif distance_right_eye_points > 10 and distance_left_eye_points > 10 and blink == True:
                                                    blink = False
                                                
                                                cv2.putText(frame, f'{int(blink_count)}', (872, 74), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 3)

                                                if blink_count >= 2:
                                                    #Take a picture when eyes are opened
                                                    if distance_right_eye_points > 15 and distance_left_eye_points > 15:
                                                        face_cut = frame_rgb[bbox_y1:bbox_y1+bbox_h, bbox_x1:bbox_x1+bbox_w]
                                                        cv2.imwrite(os.path.join(faces_folder, f'{user_reg}.png'), cv2.cvtColor(face_cut, cv2.COLOR_RGB2BGR))
                                                        step = 2
                                            else:
                                                blink_count = 0
                                        
                                        if step == 2:
                                            #Show Step_2 image
                                            h2, w2, _ = img_step2.shape
                                            frame_cp = np.copy(frame)
                                            frame[20:20+h2, 345:345+w2] = img_step2
                                            
                                            #Show Step_3 image
                                            h3, w3, _ = img_step3.shape
                                            frame = np.copy(frame_cp)
                                            frame[20:20+h3, 345:345+w3] = img_step3

                            screen_2.protocol("WM_DELETE_WINDOW", close_window_2)
                                      

        frame_PIL = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=frame_PIL)

        video_label.configure(image=img)
        video_label.image = img
        video_label.after(10, Biometric_Log)
    else:
        cap.release()

#Log function
def Log():
    global name_reg, user_reg, pass_reg, name_reg_box, username_reg_box, pass_reg_box, cap, video_label, screen_2
    name_reg, user_reg, pass_reg = name_reg_box.get(), username_reg_box.get(), pass_reg_box.get()

    #Inconmplete form revision and user registered check
    if len(name_reg) == 0 or len(user_reg) == 0 or len(pass_reg) == 0:
        print('UNCOMPLETED DATA')
    else:
        #Check if user is already in the database
        reg_user_list = os.listdir(users_folder)
        users = [user.split('.')[0] for user in reg_user_list]

        if user_reg in users:
            print("USER ALREADY EXISTS")
        else:
            info.append(name_reg)
            info.append(user_reg)
            info.append(pass_reg) 

            #Write new user on .txt user file
            with open(f'{os.path.join(users_folder, user_reg)}.txt', 'w') as f:
                f.write(name_reg + ',')
                f.write(user_reg + ',')
                f.write(pass_reg)
            
            print('USER CREATED SUCCESFULLY')
        
            #Clean Input boxes once user was created succesfully
            name_reg_box.delete(0, tk.END)
            username_reg_box.delete(0, tk.END)
            pass_reg_box.delete(0, tk.END)

            #New screen
            screen_2 = tk.Toplevel(screen)
            screen_2.title('FACE LOGIN')
            screen_2.geometry('1280x720')

            #Video Label
            video_label = tk.Label(screen_2)
            video_label.place(x=0, y=0)

            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(3, 1280)
            cap.set(4, 720)
            Biometric_Log()

def Biometric_Sign():
    global cap, video_label, blink_count, FaceCode, users, step, blink, screen_3

    if cap is not None:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=1280, height=720)
     
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret == True:
            res_face = FaceMesh.process(frame_rgb)

            #Result list
            px = []
            py =[]
            points_list = []
            if res_face.multi_face_landmarks:
                for faces in res_face.multi_face_landmarks:
                    if show_det:
                        mpDraw.draw_landmarks(frame, faces, FaceMeshObj.FACEMESH_CONTOURS, ConfigDraw, ConfigDraw)
                    
                    #Get face points info
                    for id, points in enumerate(faces.landmark):

                        h, w, c = frame.shape
                        x, y = int(points.x * w), int(points.y * h) #Points in frame coordinates
                        px.append(x)
                        py.append(y)
                        points_list.append([id, x, y])
                    
                        if len(points_list) == 468: #Mediapipe gives you 468 Keypoints
                            #Right Eye Points
                            x1, y1 = points_list[145][1:] #Up point
                            x2, y2 = points_list[159][1:] #Down point
                            distance_right_eye_points = math.hypot(x2-x1, y2-y1)

                            #Left Eye Points
                            x3, y3 = points_list[374][1:] #Up point
                            x4, y4 = points_list[386][1:] #Down point
                            distance_left_eye_points = math.hypot(x4-x3, y4-y3)

                            #Right Temple Points
                            x5, y5 = points_list[139][1:] #Up point

                            #Left Temple Points
                            x6, y6 = points_list[368][1:] #Up point

                            #Right Eyebrow
                            x7, y7 = points_list[70][1:] #Up point

                            #Left Eyebrow
                            x8, y8 = points_list[300][1:] #Up point

                            #Face detection
                            faces = face_detector.process(frame_rgb)
                            if faces.detections is not None:
                                for face in faces.detections:
                                    score = face.score[0]
                                    bbox = face.location_data.relative_bounding_box
                                    if score > recog_thres:
                                        #Bbox to pixels coordinates
                                        bbox_x1, bbox_y1, bbox_w, bbox_h = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)

                                        #apply padding
                                        offset_w = (padx/100)*bbox_w
                                        bbox_x1 = int(bbox_x1 - offset_w/2) if int(bbox_x1 - offset_w/2) > 0 else 0
                                        bbox_w = int(bbox_w + offset_w) if int(bbox_w + offset_w) > 0 else 0
                                        offset_h = (pady/100)*bbox_h
                                        bbox_y1 = int(bbox_y1 - offset_h/2) if int(bbox_y1 - offset_h/2) > 0 else 0
                                        bbox_h = int(bbox_h + offset_h/2) if int(bbox_h + offset_h/2) > 0 else 0

                                        if step == 1:
                                            #Draw rectangle
                                            cv2.rectangle(frame, (bbox_x1, bbox_y1, bbox_w, bbox_h), (255,0,0), 2)

                                            #Show Step_1 image
                                            h1, w1, _ = img_step1.shape
                                            frame_cp = np.copy(frame)
                                            frame[20:20+h1, 345:345+w1] = img_step1

                                            if x7 > x5 and x8 < x6:
                                                #The person is looking at the camera
                                                frame = frame_cp
                                                cv2.rectangle(frame, (bbox_x1, bbox_y1, bbox_w, bbox_h), (0,255,0), 2)

                                                #Show Step_11 image
                                                h11, w11, _ = img_step11.shape
                                                frame_cp = np.copy(frame)
                                                frame[20:20+h11, 345:345+w11] = img_step11

                                                #blinking counter
                                                if distance_right_eye_points <= 12 and distance_left_eye_points <= 12 and blink == False:
                                                    blink_count += 1
                                                    blink = True
                                                elif distance_right_eye_points > 10 and distance_left_eye_points > 10 and blink == True:
                                                    blink = False
                                                
                                                cv2.putText(frame, f'{int(blink_count)}', (872, 74), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 3)

                                                if blink_count >= 2:
                                                    #Detect when 2 blinks were made
                                                    if distance_right_eye_points > 13 and distance_left_eye_points > 13:
                                                        step = 2
                                            else:
                                                blink_count = 0
                                        
                                        if step == 2:                                           
                                            #Find Faces
                                            faces_locations = fr.face_locations(frame_rgb)
                                            faces_cod = fr.face_encodings(frame_rgb, faces_locations)

                                            for face_cod, faces_loc in zip(faces_cod, faces_locations):
                                                #Matching
                                                match = fr.compare_faces(FaceCode, face_cod)

                                                #Similarity
                                                sim = fr.face_distance(FaceCode, face_cod)

                                                #Get the most similar face
                                                sim_face = np.argmin(sim)

                                                if match[sim_face]:
                                                    username = users[sim_face]
                                                    screen_3.destroy()
                                                    Profile(username)

                                    #screen_3.protocol("WM_DELETE_WINDOW", close_window_3)
                                      

        frame_PIL = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=frame_PIL)

        try:
            video_label.configure(image=img)
            video_label.image = img
            video_label.after(10, Biometric_Sign)
        except:
            pass
    else:
        cap.release()

#Sign function
def Sign():
    global faces_folder, cap, video_label, screen_3, FaceCode, users, face_images

    # Faces Databases
    images_list = os.listdir(faces_folder)

    #Read Face Images and Users
    face_images = [cv2.imread(f'{os.path.join(faces_folder, img_path)}') for img_path in images_list]
    users = [os.path.splitext(username)[0] for username in images_list]

    #Face Code
    FaceCode = Code_Faces(face_images)
    
    #3rd screen
    screen_3 = tk.Toplevel(screen)
    screen_3.title('Biometric Sign Up')
    screen_3.geometry('1280x720')
    
    #Video Label
    video_label = tk.Label(screen_3)
    video_label.place(x=0, y=0)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)
    Biometric_Sign()

########################################### LAYOUT IMAGES #######################################################

img_step1 = cv2.imread(os.path.join(images_folder, 'step1.png'))
img_step1 = cv2.resize(cv2.cvtColor(img_step1, cv2.COLOR_BGR2RGB), (600,70))
img_step11 = cv2.imread(os.path.join(images_folder, 'step11.png'))
img_step11 = cv2.resize(cv2.cvtColor(img_step11, cv2.COLOR_BGR2RGB), (600,70))
img_step2 = cv2.imread(os.path.join(images_folder, 'step2.png'))
img_step2 = cv2.resize(cv2.cvtColor(img_step2, cv2.COLOR_BGR2RGB), (600,70))
img_step3 = cv2.imread(os.path.join(images_folder, 'step3.png'))
img_step3 = cv2.resize(cv2.cvtColor(img_step3, cv2.COLOR_BGR2RGB), (600,70))
#img_success = cv2.imread(os.path.join(images_folder, 'success.png'))

############################################# INTERFACES ########################################################

#Tool Draw
mpDraw = mp.solutions.drawing_utils
ConfigDraw = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

#Face Mesh
FaceMeshObj = mp.solutions.face_mesh
FaceMesh = FaceMeshObj.FaceMesh(max_num_faces=1)

#Face Detector
FaceObj = mp.solutions.face_detection
face_detector = FaceObj.FaceDetection(min_detection_confidence=0.5, model_selection=1)

#Main Window
screen = tk.Tk() #create screen
screen.title('Face Attendance App') #set title
screen.geometry('1280x720') #set dimensions

#Set background
back_image = tk.PhotoImage(file=os.path.join(images_folder, 'background.png'))
background = tk.Label(image = back_image, text='Start')
background.place(x=0, y=0, relheight=1, relwidth=1)

#Set LogIn Background
back_image_4 = tk.PhotoImage(file=os.path.join(images_folder, 'background_3.png'))

#Set register inputs (name, username, password)
name_reg_box = tk.Entry(screen, width=20,font=font.Font(family="Times", size=20))
name_reg_box.place(x=243, y=290)
username_reg_box = tk.Entry(screen, width=20,font=font.Font(family="Times", size=20))
username_reg_box.place(x=284, y=395)
pass_reg_box = tk.Entry(screen, width=20,font=font.Font(family="Times", size=20))
pass_reg_box.place(x=278, y=498)

#Set buttons
reg_button_image = Image.open(os.path.join(images_folder, 'reg_button.png'))
reg_button_image = reg_button_image.resize((240,60))
reg_button_image = ImageTk.PhotoImage(reg_button_image)
reg_button = tk.Button(screen, image = reg_button_image, command=Log, borderwidth=0)
reg_button.place(x=210, y=590)

log_button_image = Image.open(os.path.join(images_folder, 'login_button.png'))
log_button_image = log_button_image.resize((240,60))
log_button_image = ImageTk.PhotoImage(log_button_image)
log_button = tk.Button(screen, image = log_button_image, command=Sign, borderwidth=0)
log_button.place(x=850, y=590)

screen.mainloop()