import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as io
import cv2

classes = ['ignore', 'pedestrian', 'people', 'bicycle', 'car', 'van', 'truck', 'tricycle', 'awning-tricycle', 'bus', 'motor', 'others']

def read_labels_file(path):
    with open(path) as f:
        labels = [label.strip() for label in f.readlines()]
    
    return labels

def read_image_file(path):
    image = io.imread(path)
    return image

def display_image(image, figsize=(10,10)):
    plt.figure(figsize=figsize)
    plt.imshow(image)
    plt.title('Example')
    plt.show()

def display_image_w_annotations(image, annotation_list, max_annot=1000):
    for i, annot in enumerate(annotation_list):
        if i == max_annot:          
            break
        #bbox_left, bbox_top, bbox_width, bbox_height, score, object_category, truncation, occlusion = annot.split(sep=',') #String format
        bbox_left, bbox_top, bbox_width, bbox_height, score, object_category, truncation, occlusion = [int(x) for x in annot.split(sep=',')] #Int format
        image = cv2.rectangle(image, (bbox_left, bbox_top), (bbox_left + bbox_width, bbox_top + bbox_height), (0,0,255), 2)
        cv2.putText(image, classes[object_category], (bbox_left, bbox_top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    
    display_image(image)