import cv2
import numpy as np
from matplotlib import pyplot as plt



""" ----- 基本文件读取和保存 -----
"""
# 读取图片
src = 'file'                                 # 可以是绝对路径，也可以是相对路径
image = cv2.imread(src)
src2 = '/dir/dir/filename'
image2 = cv2.imwrite(src2)

# 读取视频帧
capture = cv2.VideoCapture
while True:
    ret, frame = capture.read()             # .read方法有一个返回值ret为0时说明视频结束
    if not ret:                             # ret为0时结束读取
        break
    cv2.imshow(frame)                       # 显示一帧画面
    c = cv2.waitKey(40)                     # 等待延迟
    if c == 27:                             # 当按下Esc时退出显示画面
        break

# 保存图片
savename = ''                               # 可以包含路径
cv2.imwrite(savename, image)
"""
"""



""" ------ numpy数组操作 -----
"""
array = np.zeros([3, 3, 3], dtype=np.uint32)   # 创建一个3维0矩阵 数据类型为 uint32 类型根据实际需求改变

array = np.ones([3, 3, 3], dtype=np.uint32)    # 创建一个3维元素都是1的矩阵
array[:, :, 0] = np.ones([3, 3]) * 255         # 给array第三维赋值

matrix = array.reshape([1, 9])                 # 改变矩阵形状
"""
"""



""" ----- 色彩空间 -----
"""
# opencv默认的色彩空间是BGR -- BGR取值范围都是0-255
# 其他色彩空间： HSV -- h：0-180; s:0-255; v:0-255;
#               （为什么是0-180,而不是0-360？归一化问题，0-180使用int8就可以表示,0-360会溢出）
#             HIS; YCrCb; YUV -- YUV是linux或安卓原始格式

# 色彩空间转换
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)       # 转化为灰度
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)         # 转化为hsv 其他同理

# 像素取反操作
inverse = cv2.bitwise_not(image)

# mask操作
mask = cv2.inRange(hsv, lowerb=[], upperb=[])         # 通过mask可以提取在range范围内的像素点 最好使用hsv图

# 通道分离与合并
b, g, r = cv2.split(src)
cv2.merge([b, g, r])
"""
"""



""" ----- 像素运算 ------
"""
# 加减乘除
add = cv2.add(image, image2)
sub = cv2.subtract(image, image2)
mul = cv2.multiply(image, image2)
div = cv2.divide(image, image2)

# 求平均值和方差
mean, var = cv2.meanStdDev(image)
print(mean)                                 # 均值比较低说图片明比较暗, 方差较大说明像素之间差距较大
#                                               方差较小说明图片信息量比较少

# 逻辑运算 与或非
cv2.bitwise_not(image, image2)
cv2.bitwise_and()                           # 与运算 原图和mask与运算可以加覆盖上mask
cv2.bitwise_or()                            # 或运算

# eg： 调整亮度和对比度
def contrast_brighness(image, b, c):
    h, w, ch = image.shapeb
    blank = np.zeros([h, w, ch], image.dtype)
    dst = cv2.addWeighted(image, c, blank, 1-c, b)
    cv2.imshow("contrast", dst)


contrast_brighness(image, 1.2, 10)          # 调用函数， 第二个参数为亮度值，第三个为对比度值
# 调整亮度实际上就是每个像素点加一定的值，这样像素点的值变高往[255,255,255],显得更亮（更白）
#    调整对比度实际上就是每个像素的乘一定的倍数，这样像素点之间的差异就会变大
"""
"""



""" ----- ROI与泛洪填充 ------
"""
# ROI reign of interest 感兴趣区域：从被处理的图像以方框、圆、椭圆、不规则多边形等方式勾勒出需要处理的区域
ROI = src[20:30, 100:300]           # 长，宽上的取值

# eg 将ROI区域变为灰色
def ROI_demo():
    src = 'dir/filename'
    face = src[200:400, 150:400]                            # 选取ROI区域
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)           # 转化为灰度图
    backface = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)       # 转化回BGR， 不然会缺少一个channel
    src[200:400, 150:400] = backface                        # 将ROI插回原图
    cv2.imshow("face", face)

# eg 泛洪填充颜色
def fill_color_demo(image):
    h, w = image.shape[:2]
    mask = np.zeros([h+2, w+2], np.uint8)                   # mask必须为单通道8位
    cv2.floodFill(image, mask, seedPoint=, newVal=, loDiff=, upDiff=, cv2.FLOODFILL_FIXED_RANGE)
    # seedPoint为开始填充的点，newVal为填充的颜色，loDiff\upDiff为需要填充的最低值和最高值，最后为填充模式
    # cv2.FLOODFILL_FIXED_RANGE -- 改变图像，泛洪填充
    # cv2.FLOODFILL_MASK_ONLY -- 不改变图像，只填充mask本身，忽略新的颜色值参数，mask值必须为0

"""
"""



""" ----- 模糊操作 -----
"""
# 模糊操作的基本原理：基于离散卷积
# 定义好每个卷积核，不同的核得到不同的效果 卷积核一般为奇数

# 均值模糊
cv2.blur(image, (5,5))                           # 第二个参数为卷积核的size -- (宽，长)
# 对随机噪声有很好的去噪效果

# 中值模糊
cv2.medianBlur(image, (5,5))
# 对椒盐噪声有很好的去噪效果

# 自定义卷积
cv2.filter2D(image, -1, kernel=kernal, anchor=)                    # kernal为自定义卷积核，anchor为卷积铆点
# 可以自定义卷积核 eg:
kernal = np.ones([5,5], np.float32) / 25                           # 该kernal与中值模糊效果相同
kernal = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], np.float32)       # 该kernal可以实现锐化
# 需要注意自定义kernal： 需要是奇数维数，相加小于等于1,若大于1需要除以一个数保证小于等于一（归一化）


# 高斯模糊
cv2.GaussianBlur(src, ksize=, sigmaX=)                  # ksize和sigma不需要同时设置
# 对高斯噪声有很好的去噪效果
# 二维高斯模糊处理在计算过程中一般拆分成两个一维，可以减少计算量
# eg： 3*3 需要9次乘法，一次除法   拆分成两次1*3,需要6次乘法，两次除法
"""
"""



""" ----- 边缘保留滤波 EPF -----
"""
# gi：边缘像素差异较大，不去滤波和模糊，就可以起到保留边缘的作用

# 高斯双边模糊
cv2.bilateralFilter(src, d=0, sigmaColor=100, sigmaSpace=15)             #

# 均值迁移模糊
cv2.pyrMeanShiftFiltering()
# 边缘会出现过度模糊的现象，类似油画的效果
"""
"""



""" ----- 图像直方图 -----
"""
# bin的大小 = (图像中不同象素值的个数)/(Bin的数目)

# 绘制直方图
def image_hist(image):
    """图像直方图"""
    color = ('blue', 'green', 'red')
    for i ,color in enumerate(color):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 255])
    plt.show()
# 可以直观的得到图像的特征

# 直方图均衡化
cv2.equalizeHist(image)
# 可以增强对比度，但是只能对灰度图做处理

# 局部直方图均衡化
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
dst = clahe.apply(image)


# 直方图反向投影图
def back_projection(image):
    """直方图反向投影"""
    sample = cv2.imread('target_name')
    target = cv2.imread('sample_name')
    roi_hsv = cv2.cvtColor(sample, cv2.COLOR_BGR2HSV)
    target_hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)

    cv2.imshow("sample", sample)
    cv2.imshow("target", target)

    roiHist = cv2.calcHist(roi_hsv, [0, 1], None, [180,256], [0, 180, 0, 256])
    # cv2.calcHist(images=, channels=, mask=, histSize=, ranges=)
    # histSize -- 直方图横坐标的区间数，如果为10,则横坐标分为10份，然后计算每个区间的像素点总和
    # ranges -- 指出每个区间的范围
    cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
    dst = cv2.calcBackProject(target_hsv, [0, 1], roiHist, [0, 180, 0, 256], 1)
    cv2.imshow("BackProjection", dst)
# 可以实现从target中提取出直方图与sample类似的区域，类似于扣图

"""
"""


""" ----- 模板匹配 -----
"""
# 模板匹配就是在整个图像区域发现与给定的子图像匹配的小块区域
# 需要一个模板图像T，然后需要原图像S
# 从上到下，从左到右

# 度量相似程度
# cv2.TM_SQDIFF -- 平方不同
"""
"""



""" ----- 图像二值化 -----
"""
# 全局阈值
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
print(ret)                                  # 阈值
cv2.imshow("binary", binary)
# cv2.THRESH_OTSU -- OTSU计算阈值    cv2.THRESH_TRIANGLE -- 三角阈值计算法,有单个直方图波峰时效果较好
# 23项可以自己手动设置阈值，但是后面的方法需要去掉

# 局部二值化
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=, C=10)
# 可以保留轮廓
# blockSize -- 考虑的临近像素的大小，必须为奇数
# C -- 是一个偏移量的调整值

# 超大图像二值化  首先对图像进行分割