import numpy as np
import cv2


class Pupil(object):
    """
    This class detects the iris of an eye and estimates
    the position of the pupil
    """

    def __init__(self, eye_frame, threshold):
        self.iris_frame = None
        self.threshold = threshold
        self.x = None
        self.y = None

        self.detect_iris(eye_frame)

    @staticmethod
    def image_processing(eye_frame, threshold):
        """Performs operations on the eye frame to isolate the iris

        Arguments:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else
            threshold (int): Threshold value used to binarize the eye frame

        Returns:
            A frame with a single element representing the iris
        """
        kernel = np.ones((3, 3), np.uint8)
        new_frame = cv2.bilateralFilter(eye_frame, 10, 15, 15) # Smoothing image & reducing noise https://cutt.ly/3nlMK7L
        new_frame = cv2.erode(new_frame, kernel, iterations=3) # Performing erosion to scrub boundaries https://cutt.ly/Fnl1xpx
        new_frame = cv2.threshold(new_frame, threshold, 255, cv2.THRESH_BINARY)[1] # Performing binary thresholding

        return new_frame

    def detect_iris(self, eye_frame):
        """Detects the iris and estimates the position of the iris by
        calculating the centroid.

        Arguments:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else
        """
        self.iris_frame = self.image_processing(eye_frame, self.threshold)

        contours, _ = cv2.findContours(self.iris_frame, self.contour_retrival(), self.contour_approx())[-2:] # Retriving contours https://cutt.ly/dnl06iK
        contours = sorted(contours, key=cv2.contourArea)

        try:
            moments = cv2.moments(contours[-2])             # Finding Centroid
            self.x = int(moments['m10'] / moments['m00'])
            self.y = int(moments['m01'] / moments['m00'])
        except (IndexError, ZeroDivisionError):
            pass

    def contour_retrival(self):
        return cv2.RETR_TREE
    def contour_approx(self):
        return cv2.CHAIN_APPROX_NONE # It removes all redundant points and compresses the contour, thereby saving memory.