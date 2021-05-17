IS_CLOSE_BUFFER_SIZE = 2


class _Buffer:
    def __init__(self, size=IS_CLOSE_BUFFER_SIZE, start_value=False):
        self.buffer = [start_value] * size

    def append(self, value):
        self.buffer.append(value)
        self.buffer.pop(0)

    def is_any_true(self):
        return any(self.buffer)

    def is_any_false(self):
        return not all(self.buffer)

    def __str__(self):
        return str(self.buffer)