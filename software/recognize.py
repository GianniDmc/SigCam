# -*-coding:utf-8 -*
import traceback
import numpy as np
import cv2
import glob, os, sys, time, datetime



# Function drawing the contour of the animal with the current image
def drawContour(image):
    # We retrieve the heigth and the width of the image
    height = image.getHeight()
    width = image.getWidth()


cap = cv2.VideoCapture('Test_lepton.avi')

fgbg = cv2.createBackgroundSubtractorMOG()
while(1):
    ret, frame = cap.read()
    gmask = fgbg.apply(frame)
    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()