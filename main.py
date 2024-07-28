import pyautogui as auto
import time
import keyboard as key
import random
from tkinter import *
from tkinter import messagebox
import threading

window = Tk()
window.title("JustClicker")
window.geometry('320x140')

lb_click_delay = Label(window, text='Click interval (ms):', font=("Arial Bold", 12))
lb_hotkey = Label(window, text='Hot key start/pause:', font=("Arial Bold", 12))
lb_space = Label(window, text='Space', font=("Arial Bold", 12))
lb_save = Label(window, text='Save coordinates:', font=("Arial Bold", 12))
lb_alt = Label(window, text='Tab', font=("Arial Bold", 12))

lb_click_delay.grid(column=0, row=0)
lb_hotkey.grid(column=0, row=1)
lb_space.grid(column=1, row=1)
lb_save.grid(column=0, row=3)
lb_alt.grid(column=1, row=3)

txt = Entry(window, width=7)
txt.grid(column=1, row=0)
txt.insert(0, '1000')  # Устанавливаем значение по умолчанию

random_delay = Checkbutton(window, text='Random delay')
random_delay.grid(column=2, row=0)

coordinates = []

status_label = Label(window, text='', font=("Arial Bold", 12), fg='green')
status_label.grid(column=0, row=6, columnspan=3)


def click(t):
    while isClicking:
        for coord in coordinates:
            if not isClicking:
                return
            if random_delay.var.get():
                delay = t + random.uniform(0, t)
            else:
                delay = t
            auto.moveTo(coord[0], coord[1])
            auto.click()
            time.sleep(delay)


def set_clicker():
    global isClicking
    isClicking = not isClicking
    update_button_text()
    if isClicking:
        start_click_thread()


def update_button_text():
    if isClicking:
        btn_toggle_clicker.config(text='Pause')
    else:
        btn_toggle_clicker.config(text='Start')


def main():
    while True:
        if isClicking:
            try:
                t = float(txt.get()) / 1000  # Convert to seconds
                click(t)
            except ValueError:
                messagebox.showerror('Error', 'Enter a valid Float value')
        time.sleep(0.01)


def save_coordinates():
    x, y = auto.position()
    coordinates.append((x, y))
    status_label.config(text=f'Coordinates saved: ({x}, {y})')

def start_click_thread():
    thread = threading.Thread(target=main)
    thread.daemon = True
    thread.start()

btn_reset = Button(window, text='Reset Coordinates', command=lambda: coordinates.clear(), font=("Arial Bold", 12))
btn_reset.grid(column=0, row=5)

btn_toggle_clicker = Button(window, text='Start', command=set_clicker, font=("Arial Bold", 12))
btn_toggle_clicker.grid(column=2, row=5)

txt.focus()
isClicking = False
random_delay.var = BooleanVar()
random_delay.config(variable=random_delay.var)

key.add_hotkey('space', set_clicker)
key.add_hotkey('tab', save_coordinates)

start_click_thread()  # Запуск основного потока сразу при старте программы

window.mainloop()
