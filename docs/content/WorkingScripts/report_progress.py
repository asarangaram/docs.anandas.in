#!/usr/bin/env python3

import time


class report_progress_basic:
    def __init__(self, total=None):
        self.counter = 0
        self.characters = ('|\b', '/\b', '-\b', '\\\b')
        self.i = 0
        self.total = total
        self.updater_on = True

    def update(self, lap_after=5000):
        if self.updater_on:
            if self.total and self.counter >= self.total:
                print(
                    "Incorrect setting for total, called more than , progress bar disabled", self.total)
                self.updater_on = False
            print(self.characters[self.i % 4], end='', flush=True)
            self.i = 0 if self.i == 3 else self.i+1
            self.counter = self.counter + 1
            if self.counter > 0:
                #lap_after = 5 # remove , for testing
                if (self.counter % lap_after) == 0:
                    self.lap(remove=True)
                #input()

    def lap(self, remove=False):
        if self.updater_on:
            if self.total:
                s = "  Completed {}/{}".format(self.counter, self.total)
            else:
                s = "  Completed {}".format(self.counter)
            print(s, end="")
            if remove:
                print ("\b" * len(s), end="")
            else:
                print("")


if __name__ == "__main__":
    def main():
        progress = report_progress_basic(200)
        for i in range(100):
            time.sleep(0.1)
            progress.update()
        progress.lap()
        for i in range(100):
            time.sleep(0.1)
            progress.update()

        progress.lap()
    main()
