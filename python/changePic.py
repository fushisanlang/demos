import threading
import random
import cv2
import numpy as np
import os

def changePic(frame, K=3):
    if type(frame) != np.ndarray:
        frame = np.array(frame)

    height, width, *_ = frame.shape  # 有时返回两个值，有时三个值
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_array = np.float32(frame_gray.reshape(-1))

    # 设置相关参数。
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    # 得到labels(类别)、centroids(矩心)。
    # 如第一行6个像素labels=[0,2,2,1,2,0],则意味着6个像素分别对应着 第1个矩心、第3个矩心、第3、2、3、1个矩心。
    compactness, labels, centroids = cv2.kmeans(frame_array, K, None, criteria, 10, flags)
    centroids = np.uint8(centroids)

    # labels的数个矩心以随机顺序排列，所以需要简单处理矩心.
    centroids = centroids.flatten()
    centroids_sorted = sorted(centroids)
    # 获得不同centroids的明暗程度，0最暗
    centroids_index = np.array([centroids_sorted.index(value) for value in centroids])

    bright = [abs((3 * i - 2 * K) / (3 * K)) for i in range(1, 1 + K)]
    bright_bound = bright.index(np.min(bright))
    shadow = [abs((3 * i - K) / (3 * K)) for i in range(1, 1 + K)]
    shadow_bound = shadow.index(np.min(shadow))

    labels = labels.flatten()
    # 将labels转变为实际的明暗程度列表，0最暗。
    labels = centroids_index[labels]
    # 列表解析，每2*2个像素挑选出一个，组成（height*width*灰）数组。
    labels_picked = [labels[rows * width:(rows + 1) * width:2] for rows in range(0, height, 2)]

    canvas = np.zeros((3 * height, 3 * width, 3), np.uint8)
    canvas.fill(255)  # 创建长宽为原图三倍的白色画布。

    # 因为 字体大小为0.45时，每个数字占6*6个像素，而白底画布为原图三倍
    # 所以 需要原图中每2*2个像素中挑取一个，在白底画布中由6*6像素大小的数字表示这个像素信息。
    y = 8
    for rows in labels_picked:
        x = 0
        for cols in rows:
            if cols <= shadow_bound:
                cv2.putText(canvas, str(random.randint(2, 9)),
                            (x, y), cv2.FONT_HERSHEY_PLAIN, 0.45, 1)
            elif cols <= bright_bound:
                cv2.putText(canvas, "-", (x, y),
                            cv2.FONT_HERSHEY_PLAIN, 0.4, 0, 1)
            x += 6
        y += 6

    return canvas

def ChangePic(picList):
    listLen=len(picList)
    i=0
    for pic in picList:
        if os.path.splitext(pic)[1] == ".jpg":
            img = cv2.imread(pic)
            str_img = changePic(img)
            cv2.imwrite("done/"+pic , str_img)
        i = i+1


def getFileList(path):
    picList = os.listdir(path)
    lenlist=len(picList)
    scount=lenlist/4
    scount=int(scount)
    list1=picList[0:scount]
    list2=picList[scount:scount*2]
    list3=picList[scount*2:scount*3]
    list4=picList[scount*3:]
    returnList=[list1,list2,list3,list4]
    return returnList

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, delay,lista):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
        self.lista = lista
    def run(self):
        ChangePic( self.lista)
 

picList=getFileList(".")


# 创建新线程
thread1 = myThread(1, "Thread-1", 1,picList[0])
thread2 = myThread(2, "Thread-2", 2,picList[1])
thread3 = myThread(3, "Thread-3", 2,picList[2])
thread4 = myThread(4, "Thread-4", 2,picList[3])

# 开启新线程
thread1.start()
thread2.start()
thread4.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
