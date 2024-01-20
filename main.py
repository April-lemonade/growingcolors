import random

import numpy as np
from PIL import Image


class Vertex:
    def __init__(self, x, y, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.filled = False
        self.neighbors = []


img = Image.open('./images/R.jpeg')
width, height = img.size

STARTX = int(width/2)
STARTY = int(height/2)

pixels = np.array(img)
# pixels1 = np.zeros(shape=pixels)
frontier = []
# 颜色处理
colors = list(img.getdata())
# print(len(colors))
random.shuffle(colors)  # 打乱颜色顺序
colors.sort(key=lambda color: (color[0], color[1], color[2]), reverse=True)  # 根据颜色的色调排序

# 把所有的像素转为vertex对象
vertex_grid = [[None for _ in range(width)] for _ in range(height)]
for i in range(height):
    for j in range(width):
        color = tuple(pixels[i, j])  # 将NumPy数组的元素转换为颜色元组
        vertex_grid[i][j] = Vertex(i, j, color)

# 获取每个像素的邻居
for i in range(height):
    for j in range(width):
        vertex = vertex_grid[i][j]
        # 添加邻居，确保邻居在图像边界内并排除自身
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if 0 <= nj < width and 0 <= ni < height and (di != 0 or dj != 0):
                    vertex.neighbors.append(vertex_grid[ni][nj])


# print(len(vertex_grid[1][1].neighbors))

def colorDiff(color1, color2):
    # print(color2)
    # 计算两个颜色之间的平方差
    return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2))


for c in colors:
    if len(frontier) == 0:
        pixels[STARTX, STARTY] = c
        # pixels1[STARTX, STARTY] = c
        vertex_grid[STARTX][STARTY].filled = True
        frontier = vertex_grid[STARTX][STARTY].neighbors
        # print(len(frontier))
    else:
        minp = frontier[0]
        minDiffAll = 200000
        diffs = []
        for p in frontier:
            minDiff = 200000
            for n in p.neighbors:
                if n.filled:
                    minDiff = min(minDiff, colorDiff(n.color, c))
            if minDiff < minDiffAll:
                minp = p
                minDiffAll = minDiff
        pixels[minp.x, minp.y] = c
        # pixels1[minp.x, minp.y] = c
        vertex_grid[minp.x][minp.y].filled = True
        vertex_grid[minp.x][minp.y].color = c
        frontier.remove(minp)
        for p in minp.neighbors:
            if not p.filled and not frontier.__contains__(p):
                frontier.append(p)
    print(len(frontier))

new_img = Image.fromarray(pixels)
new_img.save('./images/newnew.jpg')
