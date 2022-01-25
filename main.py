import numpy as np
import pygame
import tensorflow as tf
import win32gui
from PIL import Image
from tkinter import Tk, messagebox

width = height = 480
LEFT = 1
RIGHT = 3
white = (255,255,255)
black = (0,0,0)
drawing = False
win_name = 'handwritten digits recognizer'
model = tf.keras.models.load_model('my_model')
windows = []

def windowEnumerationHandler(hwnd, windows):
    windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def front():
    for i in windows:
        if i[1] == win_name:
            win32gui.ShowWindow(i[0],5)
            win32gui.SetForegroundWindow(i[0])
            break

def draw():
    if drawing:
        x, y = pygame.mouse.get_pos()
        pygame.draw.circle(screen, white, (x, y), 20)

def predict():
    img = pygame.surfarray.pixels2d(screen).T
    PIL_image = Image.fromarray(img).convert('RGB')
    PIL_image.thumbnail((28, 28), Image.ANTIALIAS)
    img = np.array(PIL_image)
    img = img[:,:,0] / 255.0
    predictions = model.predict(np.array([img]))
    res = 'The number is ' + str(np.argmax(predictions[0]))
    Tk().wm_withdraw()
    messagebox.showinfo(title=None, message=res)
    front()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption(win_name)
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False;
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                predict()
                screen.fill(black)

        draw()
        pygame.display.flip()
