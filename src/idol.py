import json

from src.models.pack import Pack
from src.logger import Logger

class Idol:
    def __init__(self, _bytes: list):
        self.bytes = _bytes
        self.packs = []
        self.packs_size = 3
        self.locked = '\x42'
        self.logger = Logger()

        self.__align__()
        self.__record__()
        self.__dump__()

    def __dump__(self):
        packs = []

        for pack in self.packs:
            packs.append({
                "bytes": pack.bytes,
                "index": pack.index
            })
        with open("compress.json", 'w') as f:
            f.write(json.dumps(
                {
                    "pack": packs
                }
            ))

    def __record__(self):
        buffer = []
        hash_value = None
        pack = None

        if (len(self.bytes) > self.packs_size):
            for index, byte in enumerate(self.bytes):
                if (len(buffer) == self.packs_size):
                    hash_value = hash(frozenset(buffer))
                    pack = Pack(index, buffer)
                    if (self.__recorded__(pack, index) == False):
                        self.logger.log(f"{hash_value} not recorded")
                        self.packs.append(
                            pack
                        )
                    else:
                        self.logger.log(f"{hash_value} already recorded")
                    buffer.clear()
                else:
                    buffer.append(byte)
    
    def __recorded__(self, pack: Pack, index: int):
        for index, recorded in enumerate(self.packs):
            if (recorded.bytes == pack.bytes):
                self.packs[index].record(index)
                return (True)
        return (False)

    def __align__(self):
        mod = len(self.bytes) % self.packs_size
        padding = self.packs_size - mod

        if (mod != 0):
            self.logger.log(f"{padding} align required")
            for i in range(0, self.packs_size - mod):
                self.bytes.append(self.locked)
            self.logger.log(f"bytes aligned")
        else:
            self.logger.log("no align required")