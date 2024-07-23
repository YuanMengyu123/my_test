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
    #创建一个与输入图像大小相同的二维numpy数组，标记已经访问过的像素。
    visited = np.zeros((image.shape[0], image.shape[1]), dtype=bool)

    for point in points:
        # 深度优先搜索以找到相连的线段
        x, y = point
        if not visited[y, x]:
            #如果未被访问过，就初始化一个空列表current_line_points存储当前线段的点，
            #并将当前点放入stack列表中，准备进行后续的'深度优先搜索'以找出完整的线段。
            current_line_points = []
            stack = [point]
            #逐步处理 stack 中的点，从而找出完整的线段
            while stack:
                #从 stack 中取出一个点，并将其坐标分别赋给 current_x 和 current_y
                current_x, current_y = stack.pop()
                #将该点在 visited 数组中标记为已访问
                visited[current_y, current_x] = True
                #将该点添加到 current_line_points 列表中，表示它是当前正在处理的线段的一部分。
                current_line_points.append((current_x, current_y))
                #get_neighbors 函数获取当前点 (current_x, current_y) 的邻居点
                neighbors = get_neighbors(current_x, current_y)
                for neighbor_x, neighbor_y in neighbors:
                    #如果该邻居点未被访问过（not visited[neighbor_y, neighbor_x]），
                    #并且在原始图像中该点的像素值为 0（表示属于线段，image[neighbor_y, neighbor_x] == 0）
                    #就将其添加到 stack 中，以便后续进行处理，并将其在 visited 数组中标记为已访问。
                    #目的是通过不断扩展'未访问的邻居点'，从而找出完整的线段
                    if not visited[neighbor_y, neighbor_x] and image[neighbor_y, neighbor_x] == 0:
                        stack.append((neighbor_x, neighbor_y))
                        visited[neighbor_y, neighbor_x] = True

            if len(current_line_points) >= 2:
                start_point = current_line_points[0]
                end_point = current_line_points[-1]
                length = calculate_length(current_line_points)
                line_segments.append((start_point, end_point, length))

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

image_path = 'image3.jpg'
image = load_image(image_path)
points = get_line_points(image)
line_segments = find_line_segments(points)

for i, (start, end, length) in enumerate(line_segments):
    print(f"线段 {i + 1}: 起始位置 {start}, 结束位置 {end}, 长度 {length}")