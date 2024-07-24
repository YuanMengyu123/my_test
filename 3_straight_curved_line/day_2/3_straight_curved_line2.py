import numpy as np
from PIL import Image
import math

def load_image(image_path):
    """
    加载图片并转换为灰度图像
    """
    image = Image.open(image_path).convert('L')
    return np.array(image)

def get_line_points(image):
    """
    找出可能属于线段的像素点
    """
    points = []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] == 0:  # 假设黑色为线段
                points.append((x, y))
    return points

def find_line_segments(points):
    """
    找出线段的位置和长度
    """
    line_segments = []
    visited = np.zeros((image.shape[0], image.shape[1]), dtype=bool)

    for point in points:
        x, y = point
        if not visited[y, x]:
            current_line_points = []
            stack = [point]
            while stack:
                current_x, current_y = stack.pop()
                visited[current_y, current_x] = True
                current_line_points.append((current_x, current_y))
                neighbors = get_neighbors(current_x, current_y)
                for neighbor_x, neighbor_y in neighbors:
                    if not visited[neighbor_y, neighbor_x] and image[neighbor_y, neighbor_x] == 0:
                        stack.append((neighbor_x, neighbor_y))
                        visited[neighbor_y, neighbor_x] = True

            if len(current_line_points) >= 2:
                start_point = current_line_points[0]
                end_point = current_line_points[-1]
                length = calculate_length(current_line_points)
                line_segments.append((start_point, end_point,length))

    return line_segments

def get_neighbors(x, y):
    """
    获取点的邻居坐标
    """
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < image.shape[1] - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < image.shape[0] - 1:
        neighbors.append((x, y + 1))
    return neighbors

def calculate_length(line_points):
    """
    计算线段长度
    """
    total_length = 0
    for i in range(len(line_points) - 1):
        current_point = line_points[i]
        next_point = line_points[i + 1]
        total_length += math.sqrt((next_point[0] - current_point[0])**2 + (next_point[1] - current_point[1])**2)
    return total_length

def remove_duplicate_lines(merged_lines, distance_threshold=10, angle_threshold=np.pi / 180):
    filtered_lines = []
    for line in merged_lines:
        x1, y1 = line[0]
        x2, y2 = line[1]

        if not filtered_lines:
            filtered_lines.append(line)
        else:
            duplicate = False
            for filtered_line in filtered_lines:
                fx1, fy1= filtered_line[0]
                fx2, fy2 = filtered_line[1]

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
image = load_image(image_path)
points = get_line_points(image)
line_segments = find_line_segments(points)
filtered_lines = remove_duplicate_lines(line_segments)


for i, (start, end,length) in enumerate(filtered_lines):
    print(f"线段 {i + 1}: 起始位置 {start}, 结束位置 {end},长度 {length}")