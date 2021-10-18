import nacl.encoding
import nacl.hash
import pickle

class Hashing:
    def __init__(self):
        pass

    def hashObj(b):
        HASHER = nacl.hash.sha256
        return (HASHER(pickle.dumps(b))).decode("utf-8")

    def hash(*argv):
        s = ""
        for arg in argv:
            s += str(arg) + "#"
        return s[:-1]
