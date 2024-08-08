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

            cv2.drawContours(frame, contours_green, -1, (255, 0, 0), 2)
            cv2.drawContours(frame, contours_blue, -1, (0, 255, 0), 2)
            cv2.drawContours(frame, contours_explosive, -1, (0, 0, 255), 2)

            frame = cv2.resize(frame, (width, height))

            outputfile.write(frame)

            cv2.imshow('...', frame)
            cv2.imshow('green Mask', green_mask)
            #cv2.imshow('blue Mask', blue_mask)
            #cv2.imshow('explosive Mask', explosive_mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    outputfile.release()
    cv2.destroyAllWindows()

