import sys

class FileTee(object):
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

class StringTee(object):
    def __init__(self):
        self.stdout = sys.stdout
        sys.stdout = self
        self.str_copy = ""
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
        self.str_copy += f'{data}'
        self.stdout.write(data)
    def close(self):
        sys.stdout = self.stdout
    def get_written_output_as_str(self):
        return self.str_copy
    
class LiveSlackTee(object):
    def __init__(self, app, threadTsId, channel):
        self.stdout = sys.stdout
        sys.stdout = self
        self.str_log = ""
        self.slack_app = app
        self.tsId = threadTsId
        self.channel = channel
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
        self.str_log += f'{data}'
        self.stdout.write(data)
        if self.str_log.count("\n") > 4:
            self.slack_app.client.chat_postMessage(channel=self.channel,text=self.str_log,thread_ts=self.tsId)
            self.str_log = ""
            
    def close(self):
        sys.stdout = self.stdout
    def get_written_output_as_str(self):
        return self.str_log
    
class EmpTee(object):
    def __init__(self):
        pass
    def __del__(self):
        pass
    def __enter__(self):
        return None
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type != None:
            print("Unhandled Exception exiting Tee:")
            print(exc_type, exc_value, exc_tb, sep="\n")