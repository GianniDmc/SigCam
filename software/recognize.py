# -*-coding:utf-8 -*
import traceback
import numpy as np
import cv2
import glob, os, sys, time, datetime


cap = cv2.VideoCapture('Test_lepton.mp4')

#création du masque pour enlever le background
fgbg = cv2.createBackgroundSubtractorMOG2()

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()

while(1):
    #capture de l'image de la video
    ret, frame = cap.read()

    #soustraction du background et obtention d'un nouvelle image filtrée
    gmask = fgbg.apply(frame)

    # Detecte les blobs
    keypoints = detector.detect(gmask)
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(gmask, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    contours,hierarchy = cv2.findContours(gmask, 1, 2)
    cnt = contours[0]
    epsilon = 0.1*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)

    #rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(approx)
    box = np.int0(box)
    cv2.drawContours(gmask,[box],0,(0,0,255),2)

    #Affichage de l'image
    cv2.imshow('frame',gmask)
    k = cv2.waitKey(30) & 0xff
    if k == 's':
        break

cap.release()
cv2.destroyAllWindows()