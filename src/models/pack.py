class Pack:
    def __init__(self, _id, index, _bytes):
        self.id = _id
        self.bytes = _bytes
        self.index = []

        self.record(index)

    def record(self, index):
        if (index not in self.index):
            self.index.append(index)
