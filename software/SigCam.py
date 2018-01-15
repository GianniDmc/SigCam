# coding: utf-8
import traceback
import numpy as np
import cv2
from pylepton.Lepton3 import Lepton3
import serial_transmission

def main(device = "/dev/spidev0.0"):
    a = np.zeros((120, 160, 3), dtype=np.uint8)
    lepton_buf = np.zeros((120, 160, 1), dtype=np.uint16)
    fgbg = cv2.createBackgroundSubtractorMOG2()

    # Window creation to expand them
    cv2.namedWindow('Background Subtraction',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Background Subtraction',800,600)
    cv2.namedWindow('Original Stream',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Original Stream',800,600)
    cv2.namedWindow('Threshold Processed', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Threshold Processed', 800,600)
    rectangleFound = False
    try:
        with Lepton3(device) as l:
            last_nr = 0
            while True:
                _,nr = l.capture(lepton_buf)
                if nr == last_nr:
                    # no need to redo this frame
                    continue
                last_nr = nr
                cv2.normalize(lepton_buf, lepton_buf, 0, 65535, cv2.NORM_MINMAX)
                np.right_shift(lepton_buf, 8, lepton_buf)
                a[:lepton_buf.shape[0], :lepton_buf.shape[1], :] = lepton_buf

                # Background Removing by appliying the BackgroundSubtractorMOG2
                gmask = fgbg.apply(a)

                # Image processing in binary format then refining it by erosion then dilatation
                thresh = cv2.threshold(gmask, 15, 255, cv2.THRESH_BINARY)[1]
                kernel = np.ones((2,2), np.uint8)
                thresh = cv2.erode(thresh, kernel, iterations=1)
                thresh = cv2.dilate(thresh, kernel, iterations=1)
                
                #Finding all the contours with an area bigger than 70 pixels
                _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for c in contours:
                    # if the contour is too small, ignore it
                    if cv2.contourArea(c) < 70:
                        continue
 
                    # compute the bounding box for the contour, draw it on the frame,
                    # and update the text
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(a, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    cv2.rectangle(thresh, (x, y), (x + w, y + h), (255, 255, 255), 2)

                    if(not rectangleFound):
                        #serial_transmission.serialsending("Detected","/dev/ttyUSB0")
                        print "Envoyé !"
                        rectangleFound = True
                
                # Displays the 3 steps of the image processing in 3 windows
                cv2.imshow('Original Stream',a)
                cv2.imshow('Background Subtraction',gmask)
                cv2.imshow('Threshold Processed', thresh)
                cv2.waitKey(1)
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
  from optparse import OptionParser

  usage = "usage: %prog [options] output_file[.format]"
  parser = OptionParser(usage=usage)

  parser.add_option("-d", "--device",
                    dest="device", default="/dev/spidev0.0",
                    help="specify the spi device node (might be /dev/spidev0.1 on a newer device)")

  (options, args) = parser.parse_args()

  main(device = options.device) 
