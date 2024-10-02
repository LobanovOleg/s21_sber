import ctypes
import os
import sys
import time
import ctypes.util

if sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
    CLOCK_MONOTONIC_RAW = 4

    libc_path = ctypes.util.find_library("c")
    libc = ctypes.CDLL(libc_path, use_errno=True)

    class Time(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long), ("tv_nanosec", ctypes.c_long)]

    def monotonic():
        t = Time()
        if libc.clock_gettime(CLOCK_MONOTONIC_RAW, ctypes.byref(t)) != 0:
            errno = ctypes.get_errno()
            raise OSError(errno, os.strerror(errno))
        return t.tv_sec + t.tv_nanosec / 1e9


if __name__ == "__main__":
    for _ in range(10):
        print(monotonic())
        time.sleep(0.1)
