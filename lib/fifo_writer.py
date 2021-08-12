# Class wrapper for writing the stream to a FIFO for file-like access

import os
import errno
import time
import stat

name = "./fifo_file"
# 硬盘建立一个文件，对文件进行读写，实际数据没有流入硬盘
class FIFOWriter:
    """FIFO writer class for named pipe output from the DJI headset"""
    def __init__(self):
        self.fifo_file = None# fifo file name
        self.LastError = None#
        self.Handle = None#

    def Open(self, HandleName = name):
        self.fifo_file = HandleName
        try:
            os.remove(self.fifo_file)
        except FileNotFoundError:
            pass

        # TODO: Windows could use some love here eventually.
        os.mkfifo(self.fifo_file)

        try:
            self.Handle = os.open(self.fifo_file, os.O_RDWR | os.O_NONBLOCK)
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                self.LastError = "Exception in Open(): {}".format(ex)
                return
        self.LastError = None

    def Write(self, Data):
        if self.Handle == None:
            self.Open()
            if self.LastError:
                return
        
        try:
            BytesWritten = os.write(self.Handle, Data)
        except BlockingIOError as e:
            self.LastError = "Exception in Write: {}".format(e)
            return None

        self.LastError = None
        return BytesWritten

    def Reset(self):
        # Expunge / delete / recreate the FIFO for stream resets
        if self.Handle:
            os.close(self.Handle)
            self.Handle = None

        self.Open(self.fifo_file)