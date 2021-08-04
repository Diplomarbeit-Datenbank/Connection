from pydub import AudioSegment
import numpy as np
import cv2


def get_audio_data(mp3_path):
    """

    :param mp3_path: path to the mp3 file
    :return:
    """
    a = AudioSegment.from_mp3(mp3_path)
    array = np.array(a.get_array_of_samples())
    return a.frame_rate, array


def get_image_data(image_path):
    """

    :param image_path: path to the image file
    : the image file dat in form of a numpy array
    """
    return cv2.imread(image_path)


def get_gif_data(gif_path):
    """

    :param gif_path: path to the gif file
    : the data which is required to send
    """
    image_list = list()
    gif_file = cv2.VideoCapture(gif_path)
    # 1. Get frame rate
    fps = gif_file.get(cv2.CAP_PROP_FPS)
    # 2. get the single images from the gif
    for counter in range(int(gif_file.get(7))):
        _, frame = gif_file.read()
        image_list.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # 3. Convert the images to numpy array
    im_array = np.array(image_list, np.uint8)

    return fps, im_array
