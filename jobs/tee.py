import sys
import os

class FileTee(object):
    def __init__(self, name, mode):
        self.file_name = name
        self.file = open(name, mode)
        self.stdout = sys.stdout
        sys.stdout = self
    def __del__(self):
        self.close()
    def __enter__(self):
        return self
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
    def final_result(self):
        self.close()
        data = ""
        with open(self.file_name,'r') as file:
            data = file.read()
        
        os.remove(self.file_name)
        data = f'\nYour job generated the following:\n ```{data}```'
        return data



class StringTee(object):
    def __init__(self):
        self.stdout = sys.stdout
        sys.stdout = self
        self.str_copy = ""
    def __del__(self):
        self.close()
    def __enter__(self):
        return self
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
    def final_result(self):
        data = self.get_written_output_as_str()
        data = f'\nYour job generated the following:\n ```{data}```'
        return data
    
class LiveSlackTee(object):
    def __init__(self, app, threadTsId, channel):
        self.stdout = sys.stdout
        sys.stdout = self
        self.str_log = ""
        self.buffer = ""
        self.slack_app = app
        self.tsId = threadTsId
        self.channel = channel
    def __del__(self):
        self.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type != None:
            print("Unhandled Exception exiting Tee:")
            print(exc_type, exc_value, exc_tb, sep="\n")
        self.close()
    def write(self, data):
        self.str_log += f'{data}'
        self.buffer += f'{data}'
        self.stdout.write(data)
        if self.buffer.count("\n") > 4:
            self.flush()
    def flush(self):
        if self.buffer != "":
            self.slack_app.client.chat_postMessage(channel=self.channel,text=self.buffer,thread_ts=self.tsId)
        self.buffer = ""
    def close(self):
        sys.stdout = self.stdout
        self.flush()
    def get_written_output_as_str(self):
        return self.str_log
    def final_result(self):
        return ""
    
class EmpTee(object):
    def __init__(self):
        pass
    def __del__(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type != None:
            print("Unhandled Exception exiting Tee:")
            print(exc_type, exc_value, exc_tb, sep="\n")

    def final_result(self):
        return ""