import cv2
import numpy as np
import pyautogui as pag
import time

width, height = pag.size()
center_x, center_y = width // 2, height // 2 + 60
roi_x, roi_y = 251, 345
x1 = center_x - roi_x
x2 = center_x + roi_x
y1 = center_y - roi_y
y2 = center_y + roi_y

time.sleep(5)

while True:
    frame = pag.screenshot()
    roi = frame[y1:y2, x1:x2]
    nframe = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lgb = np.array([50, 150, 150])
    hgb = np.array([80, 255, 255])
    green_mask = cv2.inRange(nframe, lgb, hgb)
    lbb = np.array([100, 150, 0])
    hbb = np.array([100, 255, 255])
    blue_mask = cv2.inRange(nframe, lbb, hbb)
    leb = np.array([160, 0, 130])
    heb = np.array([165, 5, 170])
    explosive_mask = cv2.inRange(nframe, leb, heb)
    contours_green, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_explosive, _ = cv2.findContours(explosive_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_blue:
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
            pag.click(x1 + cX, y1 + cY)
    for cnt in contours_green:
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
            pag.click(x1 + cX, y1 + cY)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

