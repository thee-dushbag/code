import sys


class Silent:
    def __init__(self, outfile=None, infile=None) -> None:
        self.ofile = outfile or "sys.stdout"
        self.ifile = infile or "sys.stdin"
        self.__open = False
        self.real = (sys.stdin, sys.stdout)
        self.silent = False

    def __enter__(self):
        self.mute()
        return self.real

    def __exit__(self, *_):
        self.unmute()

    def mute(self):
        if not self.__open:
            self._open()
        self.silent = True
        sys.stdin = self.infile
        sys.stdout = self.outfile

    def unmute(self):
        self.silent = False
        sys.stdin = self.real[0]
        sys.stdout = self.real[1]
        self._close()

    def _open(self):
        self.__open = True
        self.outfile = open(self.ofile, "w+")
        self.infile = open(self.ifile, "w+")

    def _close(self):
        if not self.outfile.closed:
            self.outfile.close()
        if not self.infile.closed:
            self.infile.close()
