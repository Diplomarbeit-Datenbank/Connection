from pygame import mixer
import numpy as np
import threading
import time
import cv2


mixer.init()

def debugging(func):
    def wrapper(image_path):
        print('This is only show the output on the screen and not on the pixle boy\n'
              '-> it is only to debug')
        func(image_path)

    return wrapper


@debugging
def run_image(image_path):
    image = cv2.imread(image_path)
    cv2.imshow(str(image_path), image)
    cv2.waitKey(0)


@debugging
def run_gif(gif_path):
    gif = cv2.VideoCapture(gif_path)
    while True:
        ret, frame = gif.read()
        if ret is False:
            break
        cv2.imshow(str(gif_path), frame)
        cv2.waitKey(200)


# for playing music

def _music_loop():
        while mixer.music.get_busy() == 1:
            pass
        print('Fin Music loop')


def run_mp3(mp3_path):
    if mixer.music.get_busy() == 1:
        mixer.music.pause()

    mixer.music.load(mp3_path)
    mixer.music.play()
    threading.Thread(target=_music_loop).start()


def pause_mp3():
    if mixer.music.get_busy() == 1:
        pause = True
        mixer.music.pause()

def unpause_mp3():
    if mixer.music.get_busy() == 0:
        pause = False
        mixer.music.unpause()
        threading.Thread(target=_music_loop).start()


def main():
    run_mp3('/home/pi/Desktop/Diplomarbeit/Sever/song.mp3')


if __name__ == '__main__':
    main()
