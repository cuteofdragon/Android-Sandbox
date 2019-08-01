import logging

class Receiver:

    def __init__(self,type):
        self.type = type

    def start(self):
        logging.error("Receiver:start() should not be called directly from superclass !")

    def stop(self):
        logging.error("Receiver:start() should not be called directly from superclass !")
