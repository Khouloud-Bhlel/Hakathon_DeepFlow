import cv2
import numpy as np


def verify_cachet(image_path):
    image = cv2.imread(image_path)
    template = cv2.imread('test_rapide.png', 0)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.3
    loc = np.where(result >= threshold)
    h, w = template.shape
    for pt in zip(*loc[::-1]):
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv2.imwrite('output_with_invalid_dates.png', image)