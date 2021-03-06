"""

    This Library is to send and receive data with the sever

    Following functions are available to send and receive:
        -> send string to client
        -> wait and get string from client
        -> wait and get numpy array from client
        -> wait and get image from client
        -> wait and store mp3 file from client
        -> wait and store gif file from client

    You see, it is mostly to receive data not to send -> The Game Frame should get the most data from the
    client and not provide it self. -> So if the user download a new gif -> The gif will be downloaded on the
    client and when this is done the client will send the gif to the Game Frame (client = End PC)

"""

from PIL import Image as _Image
import numpy as np
import pickle
import socket
import pydub
import sys
import cv2

__author__ = 'Christof Haidegger'
__date__ = '27.07.2021'
__completed__ = '29.07.2021'
__work_time__ = 'about 5 Hours'
__version__ = '1.0'
__licence__ = 'common licenced'


class Sever:
    """

        -> Sever (GameFrame) -> Able to send data and receive it
                             -> The Game Frame mostly receive data (like numpy array)
    """

    def __init__(self, show_info=True):
        self.__PORT__ = 7777
        self.time_out = 5  # set time out for five seconds
        self.show_info = show_info
        self.client_socket, self.client_addr = None, None
        self.sever_socket = self._create_sever_socket()

    def start_sever(self):
        """
        : Start the sever socket (wait for connection to client)
        """
        if self.show_info is True:
            print('Wait for connection')
        self.client_socket, self.client_addr = self.wait_for_client()
        if self.show_info is True:
            print('Client Addr: ', self.client_addr)

    def _create_sever_socket(self):
        """
        : Create the sever socket
        """
        sever_socket = socket.socket()
        sever_socket.bind(('', self.__PORT__))

        return sever_socket

    def wait_for_client(self):
        """
        : Wait for the Client (only one client will be accept)
        """
        self.sever_socket.listen(1)
        client_socket, client_addr = self.sever_socket.accept()

        return client_socket, client_addr

    def send_string(self, string):
        """
        :param string: string which is to send to the client
        """
        self.client_socket.send(bytes(str(string), 'utf8'))

    def _wait_for_data(self):
        """
        : -> Wait for data which is send from the client
          -> Properties:
                         The data which is send could be more than one information
                         When you would like to send more information send it like this:
                                            -> socket.send(data)
                                            -> socket.send(bytes(str('\n'), 'utf8'))
                                            -> socket.send(data)
                        so the you have only to send \n between the information you will send!

            The next thing is: To be sure to get no error by collecting the data the socket will be wait 5ns between
                               collecting the data
            When data collecting is finished the Sever will send the message: <end> to the client

        """
        received = list()
        if self.show_info is True:
            print('Start to get data')
        while True:
            self.client_socket.settimeout(self.time_out)
            try:
                packet = self.client_socket.recv(4096)
            except socket.timeout:
                print('Time out (there could be data lost)')
                # This happens when b'<end>' is not right received
                break
            if not packet or packet == b'<end>':
                break

            received.append(packet)

        if self.show_info is True:
            print('End to get data')

        return b"".join(received)

    def get_dict_data(self):
        """
        :return: Wait for the numpy array and return the received numpy array
        """
        received = self._wait_for_data()
        try:
            return pickle.loads(received)
        except EOFError:
            if self.show_info is True:
                print('No Data is dedected')
            # if some error happens a empty dict will be returned
            return dict()

    def store_string(self, path, string, mode='a'):
        """
        : store received string data in a text document
        """
        try:
            new_text_file = open(path, mode)
        except FileNotFoundError:
            print('No such File ore Directory', file=sys.stderr)
            return
        if self.show_info is True:
            print('received: ' + string)

        new_text_file.write(string)
        new_text_file.close()

    def set_receive_time_out(self, time_out):
        print('new time out:', float(time_out))
        self.time_out = float(time_out)

    def store_image(self, image_data, file_name):
        """
            -> Takes around 5 seconds for a Full HD Image (>200KB)
        :return: Wait for the image (numpy array) and return it
        """
        cv2.imwrite(file_name, image_data)
        if self.show_info is True:
            print('Image, ' + file_name + ' is stored')

    def store_mp3(self, frame_rate, audio_data, file_name):
        """
            -> This function takes about 40 seconds for a 2:30 minutes audio file
        :param frame_rate: the frame rate of the MP3 File
        :param audio_data: the numpy array which contains the Audio Data
        :param file_name: path to store the audio file
        :Wait for the mp3 data (numpy array) and store it under the file_name param
        """
        song = pydub.AudioSegment(np.int16(audio_data).tobytes(), frame_rate=frame_rate, sample_width=2, channels=2)
        song.export(file_name, format='mp3', bitrate='320k')
        if self.show_info is True:
            print('MP3, ' + file_name + ' is stored')

    def store_gif(self, gif_fps, gif_data, file_name):
        """
            -> This function wait for the gif data and store the gif to the given file_name (file_path)
            remember: The client had first to send the fps (duration) of the gif in string (utf8) format
                      Then the client had to send a determination (\n)
                      At least the client had to send the numpy array data with the singe images
                      (array[0] => first_image)
            -> This function takes about 6 seconds
        """
        single_images = [_Image.fromarray(img) for img in gif_data]
        single_images[0].save(file_name, save_all=True, append_images=single_images[1:], duration=gif_fps, loop=0)
        if self.show_info is True:
            print('GIF, ' + file_name + ' is stored')

    def get_dict(self):
        """
        : get a dictionary from the client
        """
        dictionary = self.get_dict_data()
        return dictionary

    def close_connection(self):
        """
        : Close the sever socket
        """
        self.sever_socket.close()


def main():
    sever = Sever()
    sever.start_sever()
    sever.close_connection()


if __name__ == '__main__':
    main()
