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

    thresh = cv2.threshold(gmask, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    

    for c in contours:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 500:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(gmask, (x, y), (x + w, y + h), (255, 255, 255), 2)

    """
    if len(contours) > 0:
        
        
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        for i in range(0,len(contours)):
            cnt = contours[i]
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(gmask,(x,y),(x+w,y+h),(0,255,0),2)
        #cv2.drawContours(gmask,[box],0,(0,255,0),2)
        #cv2.drawContours(gmask,(x,y),0,(0,255,0),2)
    """

    #Affichage de l'image
    cv2.imshow('frame',thresh)
    k = cv2.waitKey(30) & 0xff
    if k == 's':
        break

cap.release()
cv2.destroyAllWindows()