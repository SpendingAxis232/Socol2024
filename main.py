import cv2
import numpy as np

cap = cv2.VideoCapture("C://Users/N_OFFICE_5\PycharmProjects\Socol2024\Blum - Google Chrome 2024-08-05 11-12-09.mp4")

while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break





