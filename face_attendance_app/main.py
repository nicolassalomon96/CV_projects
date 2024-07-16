#Import libraries
import os
import sys
import numpy as np
import cv2
import mediapipe as mp
import face_recognition as fr
import tkinter as tk
from tkinter import font
import imutils
import math
from PIL import Image, ImageTk

#Paths
users_folder = r'.\Database\Users'
faces_folder = r'.\Database\Faces'
images_folder = r'.\Images'

#Log function
def Log():
    print("HOLA")

#Sign function
def Sign():
    print("CHAU")


info = []

#Interface

#Main Window
screen = tk.Tk() #create screen
screen.title('Face Attendance App') #set title
screen.geometry('1280x720') #set dimensions

#Set background
back_image = tk.PhotoImage(file=os.path.join(images_folder, 'background.png'))
background = tk.Label(image = back_image, text='Start')
background.place(x=0, y=0, relheight=1, relwidth=1)

#Set register inputs (name, username, password)
name_reg = tk.Entry(screen, width=20,font=font.Font(family="Times", size=20))
name_reg.place(x=243, y=290)
username_reg = tk.Entry(screen, width=20,font=font.Font(family="Times", size=20))
username_reg.place(x=284, y=395)
pass_reg = tk.Entry(screen, width=20,font=font.Font(family="Times", size=20))
pass_reg.place(x=278, y=498)

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