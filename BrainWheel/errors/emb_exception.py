from .base import BrainWheelException

class EmbException(BrainWheelException):
    pass

class InvalidDirectionError(EmbException):
    def __str__(self):
        return "Invalid Direction."