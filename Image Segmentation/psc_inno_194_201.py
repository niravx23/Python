import cv2
import mediapipe as mp
import numpy as np
import staticIMG 

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

BG_COLOR = (192, 192, 192)  # gray

img = cv2.imread("dhruuu.jpg")
str1 = "table.jpg"

choice = int(input('1 - Static image background removal\n2 - Realtime webcam bg removal\n'))
if choice == 1 :
    staticIMG.static_image_bg() 
if choice  == 2 : 
    opt =  int(input('1 -  Gaussian blur\n2 -Backgrounnd Image'))
    cap = cv2.VideoCapture(0)   

    str1= "bg1.jpg"
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=0) as selfie_segmentation:
        bg_image = None

        while cap.isOpened():

                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                results = selfie_segmentation.process(image)
                cv2.imshow('Segmentation Mask', results.segmentation_mask)

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.8 

                if opt == 1 :
                    bg_image = cv2.GaussianBlur(image,(33,33),0)
                else : 
                    bg_image = cv2.imread(str1)
                    bg_image = cv2.resize(bg_image, (640, 480))

                output_image = np.where(condition, image, bg_image)

                cv2.imshow('MediaPipe Selfie Segmentation', output_image)

                key = cv2.waitKey(1)  

                if key == ord('1') :
                    str1 = "bg1.jpg"
                if key == ord('2') : 
                    str1 = "bg2.jpg" 
                if key == ord('3') :
                    str1 = "bg3.jpg"
                if key == ord('4') :
                    str1 = "bg4.jpg"
                if key == ord('5') :
                    str1 = "bg5.jpg"
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()
