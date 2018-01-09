import traceback
import numpy as np
import cv2
from pylepton.Lepton3 import Lepton3

def main(device = "/dev/spidev0.0"):
    a = np.zeros((120, 160, 3), dtype=np.uint8)
    lepton_buf = np.zeros((120, 160, 1), dtype=np.uint16)
    fgbg = cv2.createBackgroundSubtractorMOG2()
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

                # Application BackgroundSubtractorMOG2
                gmask = fgbg.apply(a)

                thresh = cv2.threshold(gmask, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                
                # Recherche contours et traçage de rectangles pour les repérer
                _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for c in contours:
                    if cv2.contourArea(c) < 100:
                        continue

                    (x,y,w,h) = cv2.boudingRect(c)
                    cv2.rectangle(gmask, (x,y), (x + w, y + h), (255, 255, 255), 2)

                cv2.imshow('Buffer',gmask)
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
