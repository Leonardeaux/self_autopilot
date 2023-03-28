import numpy as np
import cv2
import pytesseract
import os
import matplotlib.pyplot as plt
import time
import image_processing as ip
import utils

from mss import mss
from threading import Thread


sct = mss()

# pytesseract.pytesseract.tesseract_cmd = os.environ['TESSERACT_PATH']


class GetGameCapture:
    def __init__(self):
        self.stream = sct.grab(utils.BOX)
        self.frame = np.array(self.stream)
        self.stopped = False
        self.frameGRAY = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.frameEDGE = cv2.Canny(self.frameGRAY, threshold1=200, threshold2=300)
        self.frameEDGE_BLUR = cv2.GaussianBlur(self.frameEDGE, (5, 5), 0)

        # self.frameTESSERACT = None
        self.frameLINES = None
        self.frameORIGINAL = None

    def start(self):
        Thread(target=self.get, args=()).start()
        Thread(target=self.get_lines, args=()).start()
        # Thread(target=self.get_timer, args=()).start()

        return self

    def get(self):
        while not self.stopped:
            self.stream = sct.grab(utils.BOX)
            self.frame = np.array(self.stream)
            self.frameGRAY = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.frameEDGE = cv2.Canny(self.frameGRAY, threshold1=200, threshold2=300)
            self.frameEDGE_BLUR = cv2.GaussianBlur(self.frameEDGE, (5, 5), 0)

    def get_timer(self):
        while not self.stopped:
            frame_1 = self.frame[utils.TOP_CHR:utils.BOTTOM_CHR, utils.LEFT_CHR:utils.RIGHT_CHR].copy()
            frame_1 = cv2.GaussianBlur(frame_1, (5, 5), 0)
            frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_RGB2GRAY)
            # (thresh, frame_1) = cv2.threshold(frame_1, 188, 255, cv2.THRESH_BINARY)
            self.frameTESSERACT = (255 - frame_1)
            custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789'
            if not pytesseract.image_to_string(self.frameTESSERACT, config=custom_config) == '':
                timer = pytesseract.image_to_string(self.frameTESSERACT, config=custom_config)
                # print(timer)

    def get_lines(self):
        while not self.stopped:
            (self.frameLINES, self.frameORIGINAL) = ip.process_img_avg_lines(self.frame)

    def stop(self):
        self.stopped = True


def recognition_launch():
    video_getter = GetGameCapture().start()

    while True:
        if video_getter.stopped or cv2.waitKey(1) == ord("q"):
            video_getter.stop()
            cv2.destroyAllWindows()
            break

        try:
            cv2.imshow("Video_lines", video_getter.frameLINES)
            cv2.imshow("Video_edge", video_getter.frameEDGE)
            cv2.imshow("Video_original", video_getter.frameORIGINAL)
        except Exception as e:
            print('showing images error : {}'.format(e))
            pass


if __name__ == '__main__':
    recognition_launch()
