import os
import time
import sys

def timeFilter(path, min_time):
    return os.path.getmtime(path) >= min_time

def getFileList(path, filter = None):
    fArr = []
    for r, d, f in os.walk(path):
        for i in f:
            if filter is not None: 
                if filter(os.path.join(r,i)):
                    fArr.append([r, i])
            else:
                fArr.append([r, i])
    return fArr
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('correct usage: python main.py <path> <min_epoch_time_in_sec>')
    else:
        _path = sys.argv[1]
        _min_time = float(sys.argv[2])
        for f in getFileList(_path, lambda path: timeFilter(path, _min_time)):
            print('file "' + f[1] + '" in "' + f[0] + '" has changed recently')