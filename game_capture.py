import numpy as np
import cv2
import image_processing as ip
import variables
from mss import mss
from threading import Thread
from driving_rules import not_really_an_ai


sct = mss()


class GameCapture:
    def __init__(self, vertices):
        self.vertices = vertices
        self.stream = sct.grab(variables.BOX_POR)
        self.frame = np.array(self.stream)
        self.stopped = False
        self.frameGRAY = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.frameEDGE = cv2.Canny(self.frameGRAY, threshold1=200, threshold2=300)
        self.frameEDGE_BLUR = cv2.GaussianBlur(self.frameEDGE, (5, 5), 0)
        self.frameROI_DBG = None
        self.frameROI = None
        self.frameLINES = None
        self.frameORIGINAL = None

    def start(self):
        Thread(target=self.get, args=()).start()
        Thread(target=self.get_lines, args=()).start()

        return self

    def get(self):
        while not self.stopped:
            self.stream = sct.grab(variables.BOX_POR)
            self.frame = np.array(self.stream)
            self.frameGRAY = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.frameEDGE = cv2.Canny(self.frameGRAY, threshold1=200, threshold2=300)
            self.frameEDGE_BLUR = cv2.GaussianBlur(self.frameEDGE, (5, 5), 0)
            self.frameROI = ip.roi(self.frameEDGE, self.vertices)
            self.frameROI_DBG = ip.roi(self.frame, self.vertices)

    def get_timer(self):
        """Not used anymore"""
        pass
        # while not self.stopped:
        #     frame_1 = self.frame[utils.TOP_CHR:utils.BOTTOM_CHR, utils.LEFT_CHR:utils.RIGHT_CHR].copy()
        #     frame_1 = cv2.GaussianBlur(frame_1, (5, 5), 0)
        #     frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_RGB2GRAY)
        #     # (thresh, frame_1) = cv2.threshold(frame_1, 188, 255, cv2.THRESH_BINARY)
        #     self.frameTESSERACT = (255 - frame_1)
        #     custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789'
        #     if not pytesseract.image_to_string(self.frameTESSERACT, config=custom_config) == '':
        #         timer = pytesseract.image_to_string(self.frameTESSERACT, config=custom_config)

    def get_lines(self):
        while not self.stopped:
            pass
            (self.frameLINES, self.frameORIGINAL, m1, m2) = ip.process_img_avg_lines(
                self.frame, self.vertices
            )
            not_really_an_ai(m1, m2)

    def stop(self):
        self.stopped = True


def launch_capture():
    video_getter = GameCapture(variables.VERTICES_FIRST_PERSON_ACC_POR).start()

    while True:
        if video_getter.stopped or cv2.waitKey(1) == ord("w"):
            video_getter.stop()
            cv2.destroyAllWindows()
            break

        try:
            # cv2.imshow("Video_lines", video_getter.frameLINES)
            cv2.imshow("Video_roi", video_getter.frameROI_DBG)
            # cv2.imshow("Video_original", video_getter.frameORIGINAL)
        except Exception as e:
            print("showing images error : {}".format(e))
            pass
