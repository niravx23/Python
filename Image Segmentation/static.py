import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

def static_image_bg() :
  with mp_selfie_segmentation.SelfieSegmentation(model_selection=0) as selfie_segmentation:
    str1 = input('Enter Name of Photo along with type : ')
    IMAGE_FILES = [str1]
    for idx, file in enumerate(IMAGE_FILES):
      image = cv2.imread(file)
      image_height, image_width, _ = image.shape

      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      image.flags.writeable = False
      results = selfie_segmentation.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      results = selfie_segmentation.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

      condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1

      bg_image = cv2.imread("bg2.jpg")
      bg_image = cv2.resize(bg_image, (885, 1110))

      output_image = np.where(condition, image, bg_image)
      cv2.imwrite('segmentend_image' + '.png', output_image)
