from utils.Landmarks_detector import *
from utils import utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280) #3 -> Width of the frames in the video stream
cap.set(4, 720)

# Codec and VideoWriter
codec = cv2.VideoWriter_fourcc(*'MP4V')
fps = cap.get(cv2.CAP_PROP_FPS) #10
video_writer = cv2.VideoWriter(r'.\outputs\output_fail.mp4', codec, fps, (1280,720))

detector = LandmarkDetector()

#labyrinth_png = cv2.imread(r'D:\Nicolas\Proyectos-IA\Opencv_Mediapipe\images\simple_labyrinth_v2.png', cv2.IMREAD_UNCHANGED)
labyrinth_png = cv2.imread(r'.\images\simple_labyrinth_v2.png', cv2.IMREAD_UNCHANGED)
labyrinth_png = cv2.resize(labyrinth_png, (1000, 600))

#Out frame camera variables
start_line_passed = False
end_line_passed = False
line_crossed = False

x_p, y_p = 0,0
y_pos = []
finger_tip_mask_rgb = np.zeros((720,1280,3), np.uint8)
initial_time, actual_time = 0,0

while cap.isOpened():
    
    #Import image from camera
    ret, frame = cap.read()
    image = cv2.flip(frame,1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #Detect landmarks           
    left_det, left_detections_list = detector.get_positions(image, kind='left_hand', draw=False) #kind is the opposite because the image is flipped

    if left_det and not line_crossed and not end_line_passed:
        finger_tip = detector.filter_landmark(left_detections_list, idx=8) #Get only the index position
        cv2.circle(image, center=finger_tip, radius=10, color=(255,0,0), thickness=cv2.FILLED)
                
        #Start line detection
        y_pos.append(finger_tip[1])
        if ((203 < finger_tip[0] < 273) and (88 < finger_tip[1] < 108) and finger_tip[1] >= y_pos[-2]):
        #1st and 2nd condition is used for measure if you pass the start line, 3rd condition measures the direction from which you passed the line
            start_line_passed = True
            y_pos = y_pos[-2:]
            initial_time = time.time()

        #Draw finger path on mask
        if start_line_passed:
            if x_p == 0 and y_p == 0:
                x_p, y_p = finger_tip[0], finger_tip[1]

            cv2.line(finger_tip_mask_rgb, (x_p, y_p), (finger_tip[0], finger_tip[1]), color = (0,0,255), thickness=2)
            x_p, y_p = finger_tip[0], finger_tip[1]
            actual_time = time.time()

        #End line detection
        if ((1013 < finger_tip[0] < 1083) and (555 < finger_tip[1] < 570) and start_line_passed == True):
            end_line_passed = True
            end_time = time.time()     

    #Overlay the labytinth
    image, mask = utils.overlayPNG(image, labyrinth_png, (40, int((frame.shape[1] - labyrinth_png.shape[1])/2)))
    
    #Change RGB overlay labyrinth to Binary
    image_mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    _, image_mask_binary = cv2.threshold(image_mask_gray, 128, 255, cv2.THRESH_BINARY)
    image_mask_binary_bgr = cv2.cvtColor(image_mask_binary, cv2.COLOR_GRAY2BGR)

    #Change RGB finger path to Binary
    finger_tip_mask_gray = cv2.cvtColor(finger_tip_mask_rgb, cv2.COLOR_BGR2GRAY)
    _, finger_tip_mask_binary = cv2.threshold(finger_tip_mask_gray, 58, 255, cv2.THRESH_BINARY)
    finger_tip_mask_binary_bgr = cv2.cvtColor(finger_tip_mask_binary, cv2.COLOR_GRAY2BGR)

    #Check if we touch the labyrinth's walls
    and_image = cv2.bitwise_and(image_mask_binary, finger_tip_mask_binary)
    if 255 in and_image:
        line_crossed = True
    
    #Show score
    if not end_line_passed and line_crossed:
            cv2.putText(image, 'YOU LOST!', (10,35), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
            cv2.putText(image, f'Final Score: {round(actual_time - initial_time, 2)}', (10,65), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
    elif not end_line_passed and not line_crossed:
            cv2.putText(image, f'Score: {round(actual_time - initial_time,2)}', (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
    else:
            cv2.putText(image, 'YOU WIN!', (10,35), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
            cv2.putText(image, f'Final Score: {round(end_time - initial_time, 2)}', (10,65), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

    cv2.putText(image, 'START', (210,90), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
    cv2.putText(image, 'FINISH', (1025,570), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)  
    cv2.imshow('Landmark Detector', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    video_writer.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
video_writer.release()
cv2.destroyAllWindows()