import execute_function_lib as ex
import connection_lib


class Connect:
    def __init__(self):
        """
        -> For information about the ob codes watcht in the table below
        -> construction of the opcode is always the first letter of the main words in the function which is to use
           Example: gs -> stand for: -> get_string or: gna -> stand for: -> get_numpy_array and so on....
        """
        self.pass_time_out = False
        self.sever = connection_lib.Sever()
        self.op_code_table = {'ss': self.sever.store_string,
                              'si': self.sever.store_image,
                              'sm': self.sever.store_mp3,
                              'sg': self.sever.store_gif,
                              'srto': self.sever.set_receive_time_out,
                              'cc': self.sever.close_connection,
                              'ri': ex.run_image,
                              'rg': ex.run_gif,
                              'rm': ex.run_mp3,
                              'pm': ex.pause_mp3,
                              'um': ex.unpause_mp3,
                              'sptt': self.set_pass_time_out_true,
                              'sptf': self.set_pass_time_out_false}

    def _main_connection_loop(self):
        """
        : In this loop is a strict way in step by step
          1. revieve the data in form of a dict {1. op_code, 2. parameters}
          2. get the function which is to run by name of the op_code
          3. get the args for the function by get the dict entry of args from the recieved dict
          4. execute the function which is to run with the given args
          5. send '<fin>' as string back to the client to tell him, that the function had been
             run without errors and the sever (SELF) is able to get the next date
          6. run the loop again until the client send the op_code cc -> close_connection()
        """
        while True:
            received_dict = self.sever.get_dict()
            op_code = received_dict.get('op_code')
            print('op_code=', op_code)

            args = received_dict.get('args')
            if op_code is None:
                if self.pass_time_out is False:
                    self.sever.send_string('<TimeOut>')
                continue
            function_to_run = self.op_code_table.get(op_code)

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
        """
        : start the sever which is waiting for the client and run the main connection loop
        """
        self.sever.start_sever()
        self._main_connection_loop()
    
    def set_pass_time_out_true(self):
        self.pass_time_out = True
    
    def set_pass_time_out_false(self):
        self.pass_time_out = False


def main():
    """
    : to test the software
    """
    con = Connect()
    con.connect_to_client()


if __name__ == '__main__':
    main()
