import sys

def error_message_detail(error):
    _, _, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = 'Error occured in python script name [{0}] line [{1}] error message [{2}]'.format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class BaseException(Exception):
    def __init__(self, error_message) -> None:
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message)

    def __str__(self) -> str:
        return self.error_message
    
    @staticmethod
    def raise_exc(error_message):
        base_exception = BaseException(error_message)
        print(base_exception)
