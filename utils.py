import cv2
import numpy as np

def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
    #imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)  # APPLY ADAPTIVE THRESHOLD
    ret, imgThreshold = cv2.threshold(imgBlur,127,255,cv2.THRESH_BINARY)
    return imgThreshold


#def findChessboard(imgThreshhold):
