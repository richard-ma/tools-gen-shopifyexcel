# !/usr/bin/env python
# APP Framework 1.0
import csv
import os
import sys
from chardet.universaldetector import UniversalDetector


class App:
    def __init__(self):
        self.title_line = sys.argv[0]
        self.encoding = None
        self.counter = 1
        self.workingDir = None

    def _char_detect(self, filename: str):
        detector = UniversalDetector()
        detector.reset()
        for line in open(filename, 'rb'):
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        self.encoding = detector.result['encoding']

    def printCounter(self, data=None):
        print("[%04d] Porcessing: %s" % (self.counter, str(data)))
        self.counter += 1

    def initCounter(self, value=1):
        self.counter = value

    def run(self):
        self.usage()
        self.process()

    def usage(self):
        print("*" * 80)
        print("*", " " * 76, "*")
        print(" " * ((80 - 12 - len(self.title_line)) // 2),
              self.title_line,
              " " * ((80 - 12 - len(self.title_line)) // 2))
        print("*", " " * 76, "*")
        print("*" * 80)

    def input(self, notification, default=None):
        var = input(notification)

        if len(var) == 0:
            return default
        else:
            return var

    def readTxtToList(self, filename, encoding=None):
        if encoding is None:
            self.encoding = self._char_detect(filename)
        else:
            self.encoding = encoding

        data = list()
        with open(filename, 'r+', encoding=self.encoding) as f:
            for row in f.readlines():
                # remove \n and \r
                data.append(row.replace('\n', '').replace('\r', ''))
        return data

    def readCsvToDict(self, filename, encoding=None):
        if encoding is None:
            self.encoding = self._char_detect(filename)
        else:
            self.encoding = encoding


        data = list()
        with open(filename, 'r+', encoding=self.encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def writeCsvFromDict(self, filename, data, fieldnames=None, encoding=None, newline=''):
        if encoding is None and self.encoding is not None:
            encoding = self.encoding

        if fieldnames is None:
            fieldnames = data[0].keys()

        with open(filename, 'w+', encoding=encoding, newline=newline) as f:
            writer = csv.DictWriter(f,
                                    fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def addSuffixToFilename(self, filename, suffix):
        filename, ext = os.path.splitext(filename)
        return filename + suffix + ext

    def getWorkingDir(self):
        return self.workingDir

    def setWorkingDir(self, wd):
        self.workingDir = wd
        return self.workingDir

    def setWorkingDirFromFilename(self, filename):
        return self.setWorkingDir(os.path.dirname(filename))

    def process(self):
        print("App Run!")


if __name__ == "__main__":
    app = App()
    app.run()
