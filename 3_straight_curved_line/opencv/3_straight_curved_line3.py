import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像并转换为灰度图像
def load_image(image_path):
    image = cv2.imread(image_path)
    return image
def find_line_segments(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 边缘检测
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # 霍夫变换检测线段
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
    return lines

# 去除重复的线段
def remove_duplicate_lines(lines, distance_threshold=10, angle_threshold=np.pi / 180):
    filtered_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if not filtered_lines:
            filtered_lines.append(line)
        else:
            duplicate = False
            for filtered_line in filtered_lines:
                fx1, fy1, fx2, fy2 = filtered_line[0]

                # 计算线段之间的距离和角度差异
                distance1 = np.sqrt((x1 - fx1) ** 2 + (y1 - fy1) ** 2)
                distance2 = np.sqrt((x2 - fx2) ** 2 + (y2 - fy2) ** 2)
                angle1 = np.arctan2(y2 - y1, x2 - x1)
                angle2 = np.arctan2(fy2 - fy1, fx2 - fx1)
                angle_diff = np.abs(angle1 - angle2)

                # 检查是否为重复线段
                if distance1 < distance_threshold and distance2 < distance_threshold and angle_diff < angle_threshold:
                    duplicate = True
                    break

            if not duplicate:
                filtered_lines.append(line)

    return filtered_lines

image_path = 'image3.jpg'
image=load_image(image_path)
lines = find_line_segments(image)
filtered_lines = remove_duplicate_lines(lines)

# 在图像上绘制检测到的线段
if filtered_lines is not None:
    for line in filtered_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        print(f"坐标位置:({x1}, {y1}) 到 ({x2}, {y2}) 长度: {length:.2f} 像素")

# 显示结果
cv2.imshow('Detected Line Segments',cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
cv2.waitKey()
cv2.destroyAllWindows()