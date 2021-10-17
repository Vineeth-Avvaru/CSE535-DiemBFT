class Hashing:
    def __init__(self):
        pass

    def hash(*argv):
        print("HAASHING1")
        s = ""
        for arg in argv:
            print("HAASHING2")
            s += str(arg) + "#"
        print("HAASHING3")
        return s[:-1]
