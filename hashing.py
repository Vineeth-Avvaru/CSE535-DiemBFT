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
        # # #print("HAASHING1")
        s = ""
        for arg in argv:
            # #print("HAASHING2")
            s += str(arg) + "#"
        # # #print("HAASHING3")
        return s[:-1]
        HASHER = nacl.hash.sha256
        digest = HASHER(s.encode('utf-8'), encoder=nacl.encoding.HexEncoder)
        return digest.decode('utf-8')
