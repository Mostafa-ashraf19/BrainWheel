from .base import BrainWheelException

class EmbException(BrainWheelException):
    pass

class InvalidDirectionError(EmbException):
    def __init__(self, dir):
        self.dir = dir
    def __str__(self):
        return f"Invalid Direction {self.dir}."

class InvalidSerialCharError(EmbException):
    def __init__(self, c):
        self.c = c
    def __str__(self):
        return f"Recieved Invalid Charachter {self.c}."