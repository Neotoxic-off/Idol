from src.idol import Idol

def read_file_bytes(file_path):
    with open(file_path, "rb") as file:
        byte_list = []
        byte = file.read(1)
        while byte:
            byte_list.append(byte)
            byte = file.read(1)
        return byte_list

if (__name__ == "__main__"):
    data = []
    idol = Idol()

    data = read_file_bytes("test/test.json")
    source = idol.compress(data).copy()
    decompress = idol.decompress("compress.json")

