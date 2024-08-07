import cv2
import numpy as np

first = "C://Users/N_OFFICE_5/PycharmProjects/Socol2024/Blum - Google Chrome 2024-08-05 11-12-09.mp4"
new = 'C://Users/N_OFFICE_5/PycharmProjects/Socol2024/NewBlum.mp4'
cap = cv2.VideoCapture(first)

if not cap.isOpened():
    print("Unable to open camera")

else:
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    '''
    print(width, type(width))
    print(height, type(height))
    print(fps, type(fps))
    '''
    outputfile = cv2.VideoWriter(new, fourcc, fps, (width, height))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            nframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lgb = np.array([0, 0, 0])
            hgb = np.array([0, 0, 0])
            green_mask = cv2.inRange(frame, lgb, hgb)
            lbb = np.array([0, 0, 0])
            hbb = np.array([0, 0, 0])
            blue_mask = cv2.inRange(frame, lbb, hbb)
            leb = np.array([0, 0, 0])
            heb = np.array([0, 0, 0])
            explosive_mask = cv2.inRange(frame, leb, heb)
            contours_green, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_explosive, _ = cv2.findContours(explosive_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)