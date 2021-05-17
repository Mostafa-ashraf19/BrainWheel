class EmbException(Exception):
    pass

class InvalidDirectionError(EmbException):
    def __str__(self):
        return "Invalid Direction."