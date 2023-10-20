import json

from src.models.pack import Pack
from src.logger import Logger

class Idol:
    def __init__(self):
        self.bytes = []
        self.packs = []
        self.file = "compress.json"
        self.packs_size = 3
        self.locked = 0x3773
        self.logger = Logger()

    def compress(self, _bytes):
        self.bytes = _bytes

        self.__align__()
        self.__record__()
        self.__dump__()

        return (self.bytes)

    def decompress(self, _file):
        self.file = _file
        
        self.bytes.clear()
        self.packs.clear()

        self.__load_compression__()
        self.__decompress_packs__()
        
        return (self.bytes)

    def __load_compression__(self):
        data = None
        self.logger.log("loading compression")

        with open(self.file, 'r') as f:
            data = json.loads(f.read())
            self.packs = data["packs"]

        self.logger.log(f"{len(self.packs)} packs loaded")

    def __decompress_packs__(self):
        buffer = []
        raw = []
        total = []

        for pack in self.packs:
            for index in pack["index"]:
                raw.append(pack["bytes"])
                for i, byte in enumerate(pack["bytes"]):
                    buffer.insert((index + i) - (len(pack["bytes"]) - 1), byte)
                    total.append(byte)
        self.bytes = buffer
        self.logger.log(f"{len(total)} bytes decompressed")

        with open("decompress.bin", 'w') as f:
            f.write(str(self.bytes))

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
                    "packs": packs
                }
            ))

        with open("compress.bin", 'w') as f:
            f.write(str(self.bytes))

    def __record__(self):
        buffer = []
        hash_value = None
        pack = None
        index = 0

        self.logger.log(f"{len(self.bytes)} bytes to compress")
        if (len(self.bytes) >= self.packs_size):
            self.logger.log("recording packs")
            while index < len(self.bytes):
                buffer = [self.bytes[index], self.bytes[index + 1], self.bytes[index + 2]]
                pack = Pack(index, index, buffer.copy())
                if (self.__recorded__(pack, index) == False):
                    self.packs.append(
                        pack
                    )
                buffer.clear()
                index += 3
            self.logger.log(f"{len(self.packs)} packs")

    def __recorded__(self, pack: Pack, index: int):
        for i, recorded in enumerate(self.packs):
            if (recorded.bytes == pack.bytes):
                self.packs[i].record(index)
                return (True)
        return (False)

    def __align__(self):
        mod = len(self.bytes) % self.packs_size
        padding = self.packs_size - mod

        if (mod != 0):
            self.logger.log(f"{padding} byte to align")
            for i in range(0, self.packs_size - mod):
                self.bytes.append(self.locked)
            self.logger.log(f"bytes aligned")
        else:
            self.logger.log("no align required")