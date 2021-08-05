"""

    -> This File is to run on the client

"""

import get_data_to_send
import socket
import pickle
import time
import sys

__author__ = 'Christof Haidegger'
__date__ = '20.07.2021'
__completed__ = '--.--.----'
__work_time__ = 'about 5 hours'
__version__ = '1.0'
__licence__ = 'opensource(common licenced)'



class Client:
    def __init__(self, sever_ip):
        self.__PORT__ = 7777
        self.last_send = None
        self.sever_ip = sever_ip
        self.client_socket = socket.socket()

    def connect_to_sever(self):
        """

        : Try connect to the given ip and port address
        """
        try:
            self.client_socket.connect((self.sever_ip, self.__PORT__))
        except ConnectionRefusedError:
            print('Game Frame not reachable', file=sys.stderr)

    def send_dict(self, dictionary):
        """

        :param dictionary: the dictionary which should be send to the sever
        """
        self.client_socket.send(pickle.dumps(dictionary))
        self.send_new_information()

    def send_command(self, op_code, args=None):
        """

        :param op_code: op_code to execute on the sever
        :param args:    type: tuple -> args must be a tuple!!!
        """
        if args is None:
            args = (True, True)
        image_data_dictionary = {'op_code': op_code, 'args': args}
        self.last_send = (self.send_command, args)
        self.send_dict(image_data_dictionary)
        self.wait_for_fin_data_collection()

    def send_image(self, image_path, path_to_store_on_sever):
        """

        :param image_path: path to the image which should be send
        :param path_to_store_on_sever: path where the image will be stored on the sever
        """
        image_data = get_data_to_send.get_image_data(image_path)
        image_data_dictionary = {'op_code': 'si', 'args': (image_data, path_to_store_on_sever)}
        self.last_send = (self.send_image, (image_path, path_to_store_on_sever))
        self.send_dict(image_data_dictionary)
        self.wait_for_fin_data_collection()

    def send_gif(self, gif_path, path_to_store_on_sever):
        """

        :param gif_path: path to the gif which should be send
        :param path_to_store_on_sever: path where the gif will be stored on the sever
        """
        fps, im_array = get_data_to_send.get_gif_data(gif_path)
        gif_data_dictionary = {'op_code': 'sg', 'args': (fps, im_array, path_to_store_on_sever)}
        self.last_send = (self.send_gif, (gif_path, path_to_store_on_sever))
        self.send_dict(gif_data_dictionary)
        self.wait_for_fin_data_collection()

    def send_mp3(self, mp3_path, path_to_store_on_sever):
        """

        :param mp3_path: audio file which should be send (mp3 only)
        :param path_to_store_on_sever: path where the mp3 File will be stored on the sever
        """
        rate, audio_data = get_data_to_send.get_audio_data(mp3_path)
        audio_data_dictionary = {'op_code': 'sm', 'args': (rate, audio_data, path_to_store_on_sever)}
        self.last_send = (self.send_mp3, (mp3_path, path_to_store_on_sever))
        self.send_dict(audio_data_dictionary)
        self.wait_for_fin_data_collection()

    def send_string(self, string, path_to_store_on_sever, writing_mode='w'):
        """

        :param string: string which is to send
        :param path_to_store_on_sever: path where the string will be stored on the sever (the string will be stored in a
                                       text file
        :param writing_mode: mode to write (assert 'a' or 'w' or 'r+' -> r+ is a bad solution!
        """
        string_data_dictionary = {'op_code': 'ss', 'args': (path_to_store_on_sever, string, writing_mode)}
        self.last_send = (self.send_string, (string, path_to_store_on_sever, writing_mode))
        self.send_dict(string_data_dictionary)
        self.wait_for_fin_data_collection()

    def send_receive_time_out(self, time_out):
        """

        :param time_out: new time out for receive data for the sever
        -> Send the new time out data to the sever
        """
        data_dictionary = {'op_code': 'srto', 'args': (time_out, )}
        self.last_send = (self.send_receive_time_out, (time_out, ))
        self.send_dict(data_dictionary)
        self.wait_for_fin_data_collection()

    def close_connection(self, wait=0.5):
        """

        :param wait: seconds to wait before closing the connection
        -> close the connection on the sever and on the client side (latency: max0.5sec between sever and client)
        """
        close_connection_dictionary = {'op_code': 'cc', 'args': (True, True)}
        self.send_dict(close_connection_dictionary)
        time.sleep(wait)
        self.client_socket.close()

    def send_new_information(self, wait=1):
        """

        :param wait: time to wait before sending the new data
        """
        time.sleep(wait)
        self.client_socket.send(bytes(str('<end>'), 'utf8'))

    def get_string(self):
        """

        :return: return a string which is send from the sever to the client
        """
        received = self.client_socket.recv(4096)
        return str(received, 'utf8')

    def wait_for_fin_data_collection(self):
        """

        -> Wait for the sever, until the sever send <fin> which means, that the sever had been the data fin collect and
           the function which is to run is completed run without any error
        """
        print('wait')
        while True:
            info = self.get_string()
            print('info:', info)
            if info == '<fin>':
                break

            if info == '':
                print('Sever unreachable')
                break

            if info.find('<TimeOut>') != -1:
                print('Information will be resend in one sec')
                time.sleep(1)
                self.last_send[0](*self.last_send[1])
                break
        print('end wait')


def main():
    # to test the program:
    ip = '169.254.92.29'

    con = Client(sever_ip=ip)
    print('Try connect to sever')
    con.connect_to_sever()
    print('connected')

    # con.send_gif('spongebob.gif', 'spongebob.gif')
    # con.send_mp3('audio.mp3', 'mood.mp3')
    # con.send_receive_time_out(10)
    # con.send_mp3('audio.mp3', 'mood.mp3')
    con.send_command('rm', ('mood.mp3', ))
    con.close_connection()


if __name__ == '__main__':
    main()
