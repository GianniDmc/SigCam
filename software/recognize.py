import numpy as np
import cv2
import glob, os, sys, time, datetime



# Function drawing the contour of the animal with the current image
def drawContour(image):
    # We retrieve the heigth and the width of the image
    height = image.getHeight()
    width = image.getWidth()

    