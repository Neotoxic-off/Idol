import random

from src.idol import Idol

if (__name__ == "__main__"):
    values = [ 62, 56, 26, 52, 99, 39, 74, 20 ]
    idol = Idol()

    source = idol.compress(values).copy()
    decompress = idol.decompress("compress.json")

    if (source == decompress):
        print("SUCCESS")
    else:
        print("FAIL")
