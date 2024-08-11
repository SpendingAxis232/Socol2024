import pygetwindow as gw
import pyautogui
import time
import keyboard
import random
import cv2
import numpy as np


def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()


def main():
    window_name = None
    windows_list = gw.getAllTitles()
    for title in windows_list:
        if "Telegram Web" in title:
            window_name = title
            break

    if not window_name:
        print(f"[❌] | Нужное окно не найдено!")
        return

    print(f"[✅] | Окно найдено - {window_name}")
    browser_window = gw.getWindowsWithTitle(window_name)[0]

    start_input = input('[✅] | Введите 1 для начала:')
    if start_input != '1':
        print("[❌] | Неверное значение, программа завершен")
        return

    print("Нажмите 'q' для паузы/возобновления работы")

    roi_width = 500
    roi_height = 400

    paused = False
    while True:
        if keyboard.is_pressed('q'):
            paused = not paused
            if paused:
                print('[✅] | Пауза')
            else:
                print('[✅] | Продолжение работы')
            time.sleep(0.2)

        if paused:
            continue

        try:
            if browser_window.isMinimized or not browser_window.isActive:
                print("[❌] | Окно свернуто или неактивно")
                time.sleep(1)
                continue

            browser_window.activate()
            window_rect = (
                browser_window.left, browser_window.top, browser_window.width, browser_window.height
            )

            roi_x1 = window_rect[0] + (window_rect[2] // 2) - (roi_width // 2)
            roi_y1 = window_rect[1] + (window_rect[3] // 2) - (roi_height // 2)

            screenshot = pyautogui.screenshot(region=(roi_x1, roi_y1, roi_width, roi_height))

            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lgb = np.array([35, 200, 200])
            hgb = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv_frame, lgb, hgb)

            lbb = np.array([85, 200, 200])
            hbb = np.array([125, 255, 255])
            blue_mask = cv2.inRange(hsv_frame, lbb, hbb)

            combined_mask = cv2.bitwise_or(green_mask, blue_mask)

            contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            min_contour_area = 300

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < min_contour_area:
                    continue

                M = cv2.moments(cnt)
                if M['m00'] != 0:
                    cX = int(M['m10'] / M['m00'])
                    cY = int(M['m01'] / M['m00'])
                    screen_x = roi_x1 + cX
                    screen_y = roi_y1 + cY
                    click(screen_x, screen_y)

        except Exception as e:
            print(f"[❌] | {e}")
            break


if keyboard.is_pressed('q'):
    print("Работа завершена!")


if __name__ == "__main__":
    main()
