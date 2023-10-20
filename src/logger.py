import json
from datetime import datetime

class Logger:
    def __init__(self):
        self.logs = []
        self.builtin = (
            str,
            int,
            float,
            list,
            dict
        )

    def __get_date__(self):
        return (datetime.now().strftime("%H:%M:%S"))

    def log(self, message):
        record = "[{}] {}".format(
            self.__get_date__(),
            message
        )

        print(record)
