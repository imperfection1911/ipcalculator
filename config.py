import os
import configparser


class Configuration:

    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')

    def read_param(self, section, param):
        return self.config.get(section, param)
