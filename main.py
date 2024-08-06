import cv2
import numpy as np
import pyautogui
from pynput import keyboard
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import random

# Диапазон смещения курсора от центра снежинки вниз
RAND_MIN = 5  # Мин пикселей
RAND_MAX = 10  # Макс пикселей

# Кнопка активации/деактивации кликера
ACTIVE_BTN = keyboard.Key.ctrl_r
# Кнопка завершения программы
EXIT_BTN = keyboard.Key.backspace

# Параметры захвата экрана или видео
# region = (0, 0, 280, 380)  # Для видеозаписи это может быть неактуально
element_lower = np.array([45, 75, 75])
element_upper = np.array([75, 255, 255])

# Диапазоны для темно-зеленого цвета
dark_green_lower = np.array([6, 22, 0])
dark_green_upper = np.array([85, 255, 125])

# Минимальная и максимальная площадь контура для фильтрации
min_contour_area = 100
max_contour_area = 1000

clicking_enabled = False
program_running = True
executor = ThreadPoolExecutor(max_workers=10)

video_source = 'C://Users/N_OFFICE_5/PycharmProjects/Socol2024/Blum - Google Chrome 2024-08-05 11-12-09.mp4'  # Замените на путь к вашему видеофайлу



def on_press(key):
    global clicking_enabled, program_running
    try:
        if key == ACTIVE_BTN:
            clicking_enabled = not clicking_enabled
            print(f"Clicking enabled: {clicking_enabled}")
        elif key == EXIT_BTN:
            program_running = False
            print("Exiting program...")
            return False  # Останавливает слушатель клавиш
    except AttributeError:
        pass


def process_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Создаем основную маску
    mask = cv2.inRange(hsv, element_lower, element_upper)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Фильтруем контуры по площади и убираем вложенные контуры
    filtered_contours = []
    for i, cnt in enumerate(contours):
        if min_contour_area <= cv2.contourArea(cnt) <= max_contour_area and hierarchy[0][i][3] == -1:
            filtered_contours.append(cnt)
    return filtered_contours


# def click_on_position(screen_x, screen_y):
#     global clicking_enabled
#     if clicking_enabled:
#         pyautogui.click(screen_x, screen_y + random.randint(RAND_MIN, RAND_MAX))


# def click_element_contours(contours):
#     global clicking_enabled
#     for cnt in contours:
#         if not clicking_enabled:
#             break  # Прекращаем обработку контуров, если клики отключены
#         (x, y, w, h) = cv2.boundingRect(cnt)
#         center_x = x + w // 2
#         center_y = y + h // 2
#         # screen_x и screen_y можно адаптировать для видео
#         screen_x = region[0] + center_x
#         screen_y = region[1] + center_y
#         executor.submit(click_on_position, screen_x, screen_y)  # Асинхронный клик


def capture_and_process_video():
    global program_running
    cap = cv2.VideoCapture(video_source)

    while program_running:
        ret, frame = cap.read()
        if not ret:
            break  # Если кадры заканчиваются, выходим из цикла

        contours = process_frame(frame)

        # Удаляем темно-зеленый цвет
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dark_green_mask = cv2.inRange(hsv_frame, dark_green_lower, dark_green_upper)
        frame[dark_green_mask > 0] = (0, 0, 0)  # Заменяем темно-зеленый цвет на черный

        # Рисуем контуры на кадре
        cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)


        # Для визуализации захваченной области с контурами
        cv2.imshow("Video Capture", frame)
        cv2.waitKey(1)  # Обновляем изображение
        time.sleep(0.05)
        # if clicking_enabled:
        #     click_element_contours(contours)

    cap.release()
    cv2.destroyAllWindows()
    print("Capture and processing thread terminated")


listener = keyboard.Listener(on_press=on_press)
listener.start()

capture_thread = threading.Thread(target=capture_and_process_video)
capture_thread.start()

try:
    listener.join()
    capture_thread.join()
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    print("Program terminated")



