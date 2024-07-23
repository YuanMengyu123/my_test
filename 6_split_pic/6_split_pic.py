import cv2
import numpy as np

def segment_disk(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY_INV)

    # 查找轮廓
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 对轮廓面积进行排序
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    cv2.drawContours(image, [contours[0]], -1, (0, 255, 0), 2)

    cv2.imshow('Segmented Disk', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = 'image6.JPG'
segment_disk(image_path)