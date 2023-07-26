import numpy as np
import matplotlib.pyplot as plt
import cv2
import mediapipe as mp
import math
import time

def overlayPNG(image_back, image_front, location=(0,0), return_mask=True):

    #Get background and front image shapes
    back_h, back_w = image_back.shape[:2]
    front_h, front_w = image_front.shape[:2]

    #Extract alpha channel as mask and base BGR images
    front_bgr = image_front[:,:,:3]
    front_mask = image_front[:,:,3]

    #Overlay both images
    image_new = image_back.copy()
    image_new[location[0]: location[0] + front_h, location[1]: location[1] + front_w] = front_bgr

    mask_new = np.zeros((back_h, back_w), dtype=np.uint8)
    mask_new[location[0]: location[0] + front_h, location[1]: location[1] + front_w] = front_mask
    mask_new = cv2.cvtColor(mask_new, cv2.COLOR_GRAY2BGR)

    result = np.where(mask_new==255, image_new, image_back)

    if return_mask:
        return result, mask_new
    else:
        return result