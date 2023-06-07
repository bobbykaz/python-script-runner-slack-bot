import sys

class Tee(object):
    def __init__(self, name, mode):
        self.file = open(name, mode)
        self.stdout = sys.stdout
        sys.stdout = self
    def __del__(self):
        self.close()
    def __enter__(self):
        return None
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type != None:
            print("Unhandled Exception exiting Tee:")
            print(exc_type, exc_value, exc_tb, sep="\n")
        self.close()
    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
    def flush(self):
        self.file.flush()
    def close(self):
        sys.stdout = self.stdout
        self.file.close()