from pyautogui import *
import pygetwindow as gw
import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller

mouse = Controller()
time.sleep(0.5)



def is_gray(r, g, b, threshold=15):
    return abs(r - g) < threshold and abs(b - r) < threshold

#
def check_surrounding_for_gray(scrn, x, y, width, height, distance=70):
    for dx in [-distance, distance + 1, 5]:
        for dy in [-distance, distance + 1, 5]:
            if 0 <= x + dx < width and 0 <= y + dy < height:
                r, g, b = scrn.getpixel((x + dx, y + dy))
                if is_gray(r, g, b):
                    return True
    return False


def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

#
# Вывод всех доступных окон
# print("[✅] | Доступные окна:")
# for window in gw.getAllWindows():
#     print(f" - {window.title}")

windows_list = gw.getAllWindows()
print(windows_list)
# exit()

window_name = None
for window in windows_list:
    print(window.title)
    if"Telegram Web" in window.title:
        window_name = window.title
        break

if not window_name:
    print(f"[❌] | Нужное окно не найдено!")
    exit()

# window_name = input('\n[✅] | Введите название окна (1 - Blum-SunBrowser): ')

# if window_name == '1':
#     window_name = "Blum - SunBrowser"

# check = gw.getWindowsWithTitle(window_name)
# if not check:
#     print(f"[❌] | Окно - {window_name} не найдено!")
# else:

print(f"[✅] | Окно найдено - {window_name}")
start_input = input('[✅] | Введите 1 для начала: ')
if start_input != '1':
    print("[❌] | Неверное значение, программа завершена.")
    exit()

print("Нажмите 'q' для паузы.")
browser_window = gw.getWindowsWithTitle(window_name)[0]
paused = False
start_timer = False
timer_start_time = None
random_time = random.randint(50, 51)


while True:
    if keyboard.is_pressed('q'):
        paused = not paused
        start_timer = not paused
        if paused:
            print('[✅] | Пауза.')
        else:
            timer_start_time = time.time()
            print('[✅] | Продолжение работы.')
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        browser_window.left, browser_window.top, browser_window.width, browser_window.height
    )

    if browser_window != []:
        try:
            browser_window.activate()
        except:
            browser_window.minimize()
            browser_window.restore()

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    width, height = scrn.size
    pixel_found = False

    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = scrn.getpixel((x, y))

            if is_gray(r, g, b):
                continue

            if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y
                click(screen_x + 4, screen_y)
                time.sleep(0.01)
                pixel_found = True
                last_found_time = time.time()
                break

            if (r in range(100, 175)) and (g in range(200, 255)) and (b in range(200, 255)):
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y
                click(screen_x + 4, screen_y)
                time.sleep(0.01)
                pixel_found = True
                last_found_time = time.time()
                break


print('[✅] | Остановлено.')
