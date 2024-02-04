import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as io
import cv2
import sys

#classes = ['ignore', 'pedestrian', 'people', 'bicycle', 'car', 'van', 'truck', 'tricycle', 'awning-tricycle', 'bus', 'motor', 'others']
classes = ['pedestrian', 'people', 'bicycle', 'car', 'van', 'truck', 'tricycle', 'awning-tricycle', 'bus', 'motor']

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

def display_image_w_annotations_original(image, annotation_list, max_annot=1000):
    #Original dataset annotation format: bbox_left, bbox_top, bbox_width, bbox_height, score, object_category, truncation, occlusion
    image_cp = image.copy()
    for i, annot in enumerate(annotation_list):
        if i == max_annot:          
            break
        #bbox_left, bbox_top, bbox_width, bbox_height, score, object_category, truncation, occlusion = annot.split(sep=',') #String format
        bbox_left, bbox_top, bbox_width, bbox_height, score, object_category, truncation, occlusion = [int(x) for x in annot.split(sep=',')] #Int format
        image_cp = cv2.rectangle(image_cp, (bbox_left, bbox_top), (bbox_left + bbox_width, bbox_top + bbox_height), (0,0,255), 2)
        cv2.putText(image_cp, classes[object_category], (bbox_left, bbox_top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    
    display_image(image_cp)

def display_image_w_annotations_YOLO(image, annotation_list, max_annot=1000):
    #YOLO dataset annotation: class_id, center_x, center_y, width, height
    image_cp = image.copy()
    image_height, image_width = image.shape[0], image.shape[1]
    for i, annot in enumerate(annotation_list):
        if i == max_annot:          
            break
        class_id, center_x, center_y, width, height = [float(x) for x in annot.split(sep=' ')] #Int format
        center_x = int(center_x * image_width)
        center_y = int(center_y * image_height)
        width = int(width * image_width)
        height = int(height * image_height)
        image_cp = cv2.rectangle(image_cp, (center_x-width//2, center_y-height//2), (center_x+width//2, center_y+height//2), (0,0,255), 2)
        cv2.putText(image_cp, classes[int(class_id)], (center_x-width//2, center_y-height//2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        
    display_image(image_cp)

#Image resize mantaining de aspect ratio
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def draw_boxes(image, result_boxes):
    colors = {'pedestrian':(0,255,0), 'people':(0,255,0), 'bicycle':(0,0,255), 'car':(255,0,0), 'van':(255,255,0), 'truck':(255,0,255),
              'tricycle':(0,0,255), 'awning-tricycle':(0,0,255), 'bus':(255,255,0), 'motor':(0,0,255)}
    image_cp = np.copy(image)
    
    if len(result_boxes) > 0:
        for box in result_boxes:
            box_xyxy = box.xyxy[0].detach().cpu().numpy().astype(int)
            output = cv2.rectangle(image_cp,(box_xyxy[0],box_xyxy[1]),(box_xyxy[2],box_xyxy[3]),colors[list(colors.keys())[int(box.cls.item())]], 2)
            output = cv2.putText(output, list(colors.keys())[int(box.cls.item())], (box_xyxy[0],box_xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,  1, colors[list(colors.keys())[int(box.cls.item())]], 2)
    else:
        print("NO DETECTONS FOUND")
        output = []
    return output

def predict(model, image, mode='detection', plot=False, conf_thresh=0.5, objects=None, imgsz=704):
    #conf_thresh = confidence threshold for object detection
    #objects = LIST of objects to detect

    number_class_list = []
    if objects!=None:
        if objects!=['all']:
            for object in objects: 
                number_class_list.append(classes.index(object))
        elif objects == ['all']:
            number_class_list = list(range(len(classes)))
    
    results = model.predict(image, verbose=False, conf=conf_thresh, classes=number_class_list, imgsz=imgsz)
    result_boxes = []
    result_masks = []
    result_probs = []
    results_images = []

    for result in results:
        if plot:
            image_bgr = result.plot()
            results_images.append(image_bgr) #Image RGB

        if mode=='detection' and plot==True:
            # detection
            result_boxes.append(result.boxes)
            #print(result.boxes.xyxy)  # box with xyxy format, (N, 4)
            #print(result.boxes.xywh)  # box with xywh format, (N, 4)
            #print(result.boxes.xyxyn)  # box with xyxy format but normalized, (N, 4)
            #print(result.boxes.xywhn)  # box with xywh format but normalized, (N, 4)
            #print(result.boxes.conf)  # confidence score, (N, 1)
            #print(result.boxes.cls)  # cls, (N, 1)
            return result_boxes, results_images
        elif mode=='detection' and plot==False:
            result_boxes.append(result.boxes)
            return result_boxes
        
        elif mode=='segmentation' and plot==True:
            # segmentation
            result_masks.append(result.masks)
            #print(result.masks.masks)     # masks, (N, H, W)
            #print(result.masks.segments)  # bounding coordinates of masks, List[segment] * N
            return result_masks, results_images
        elif mode=='segmentation' and plot==False:
            result_masks.append(result.masks)
            return result_masks  

        elif mode=='classification' and plot==True:
            # classification
            result_probs.append(result.probs)
            #print(result.probs)     # cls prob, (num_class, )
            return result_probs, results_images
        elif mode=='classification' and plot==False:
            # classification
            result_probs.append(result.probs)
            return result_probs
        
        else:
            print('Wrong mode selected')