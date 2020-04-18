import os
import time
import sys
import shutil

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

def copyFile(src, target, utime):
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(src, target)
    os.utime(target, (utime, utime))

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) == 4 or len(sys.argv) > 5:
        print('correct usage: python main.py <path> <min_epoch_time_in_sec> [<target> <modified_epoch_time_in_sec>]')
    else:
        _path = sys.argv[1]
        _min_time = float(sys.argv[2])
        _target = None
        _utime = None
        if len(sys.argv) == 5:
            _target = sys.argv[3]
            _utime = float(sys.argv[4])
        for f in getFileList(_path, lambda path: timeFilter(path, _min_time)):
            print('file "' + f[1] + '" in "' + f[0] + '" has changed recently')
            if _target is not None:
                _file_src = os.path.join(f[0], f[1])
                _file_target = os.path.join(_target, os.path.relpath(_file_src, _path) )
                copyFile(_file_src, _file_target, _utime)
                print('file "' + f[1] + '" in "' + f[0] + '" has been copied to ' + _file_target)