import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from scipy.optimize import least_squares
import math

def load_image(image_path):
    """
    加载图片并转换为灰度图像
    """
    image = Image.open(image_path).convert('L')
    return np.array(image)

def find_arc_points(image):
    """
    找出可能属于圆弧的像素点（假设黑色表示圆弧）
    """
    points = []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] == 0:  # 假设黑色为圆弧
                points.append([x, y])
    return np.array(points)

def arc_function(params, x, y):
    """
    圆弧的方程
    这个差值反映了点(x, y)相对于圆弧的位置偏差。如果这个差值为0，说明点(x, y)正好在圆弧上；
    如果差值大于0，说明点在圆弧外部；如果差值小于0，说明点在圆弧内部
    """
    center_x, center_y, radius = params
    return (x - center_x) ** 2 + (y - center_y) ** 2 - radius ** 2

def residual(params, points):
    """
    计算残差
    """
    return [arc_function(params, p[0], p[1]) for p in points]

def fit_arc(points):
    """
    拟合圆弧
    """
    # 这是对圆弧参数的初始猜测。
    # 通常，取点集的平均 x 坐标和平均 y 坐标作为圆心的初始估计位置，100为半径的初始估计值
    initial_guess = [points[:, 0].mean(), points[:, 1].mean(), 100]
    # residual 是一个自定义的函数，用于计算每个点到估计圆弧的偏差（残差）。
    # initial_guess 是优化的起始参数值。
    # args=(points,) 作为额外的固定参数传递给 residual 函数
    # least_squares 函数会不断调整 params 的值，使得通过 residual 函数计算得到的残差最小化。
    # 从而找到最优的圆弧参数，并将结果存储在 result.x 中返回。
    result = least_squares(residual, initial_guess, args=(points,))
    return result.x


image_path = 'image5.jpg'
image = load_image(image_path)
points = find_arc_points(image)
arc_params = fit_arc(points)

center_x, center_y, radius = arc_params
print(f"圆弧中心坐标: ({center_x}, {center_y})，半径: {radius}")

# 提取 x 和 y 坐标
x_coords = points[:, 0]
y_coords = points[:, 1]

# 绘制原始图像
plt.imshow(image, cmap='gray')

# 绘制圆弧
plt.plot(x_coords, y_coords, color='red')

# 显示并保存图像
plt.savefig('out5.jpg')
plt.show()