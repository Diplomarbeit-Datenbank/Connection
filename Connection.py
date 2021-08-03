import connection_lib


class Connect:
    def __init__(self):
        """
        -> For information about the ob codes watcht in the table below
        -> construction of the opcode is always the first letter of the main words in the function which is to use
           Example: gs -> stand for: -> get_string or: gna -> stand for: -> get_numpy_array and so on....
        """
        self.sever = connection_lib.Sever()
        self.op_code_table = {'ss': self.sever.store_string,
                              'si': self.sever.store_image,
                              'sm': self.sever.store_mp3,
                              'sg': self.sever.store_gif,
                              'srto': self.sever.set_receive_time_out,
                              'cc': self.sever.close_connection}

    def _main_connection_loop(self):
        while True:
            received_dict = self.sever.get_dict()
            op_code = received_dict.get('op_code')
            print('op_code=', op_code)
            args = received_dict.get('args')
            if op_code is None:
                self.sever.send_string('<TimeOut>')
                continue
            function_to_run = self.op_code_table.get(op_code)
            # print('args=', args)
            if len(args) == 1:
                function_to_run(args[0])
            elif args[0] is True:
                function_to_run()
                if op_code == 'cc':
                    print('close connection')
                    break
            else:
                function_to_run(*args)
            print('fin')
            self.sever.send_string('<fin>')

    def connect_to_client(self):
        self.sever.start_sever()
        self._main_connection_loop()


def main():
    con = Connect()
    con.connect_to_client()


if __name__ == '__main__':
    main()
