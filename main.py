import os
import time
import sys
import shutil

# filter which asserts if the path was updated on or after the given time
def timeFilter(path, min_time):
    return os.path.getmtime(path) >= min_time

# Returns array of files/folders which pass through the given filter.
# If no filter is given then all the files pass through. If the folder passes through the filter
# then the folder isn't traversed further
def getFileList(path, filter = None):
    fArr = []
    for r, d, f in os.walk(path):
        isDirectoryTraversed = False
        if r != path:
            if filter is not None: 
                if filter(r):
                    fArr.append([r, None])
                    isDirectoryTraversed = True
            else:
                fArr.append([r, None])
                isDirectoryTraversed = True
        if isDirectoryTraversed is False:
            for i in f:
                if filter is not None: 
                    if filter(os.path.join(r,i)):
                        fArr.append([r, i])
                else:
                    fArr.append([r, i])
    return fArr

def copyFile(src, target, utime, is_dir = False):
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if is_dir is False:
        shutil.copyfile(src, target)
        os.utime(target, (utime, utime))
        return True
    else:
        if os.path.isdir(target) is False:
            shutil.copytree(src, target)
            os.utime(target, (utime, utime))
            return True
    return False


def statusMessage(f):
    if f[1] is not None:
        print('file: ' + os.path.join(f[0], f[1]))
    else:
        print('folder: ' + f[0])

def getPath(f):
    if f[1] is not None:
        _file_src = os.path.join(f[0], f[1])
    else:
        _file_src = f[0]
    return _file_src

def actionOnTarget(f, root_path, _target, _utime):
    _file_src = getPath(f)
    _file_target = os.path.join(_target, os.path.relpath(_file_src, root_path) )
    if f[1] is not None:
        is_dir = False
        if copyFile(_file_src, _file_target, _utime, is_dir) is True:
            print('file "' + f[1] + '" in "' + f[0] + '" has been copied to ' + _file_target)
    else:
        is_dir = True
        if copyFile(_file_src, _file_target, _utime, is_dir) is True:
            print('folder "' + f[0] + '" has been copied to ' + _file_target)
        else:
            print('(copy failure): folder "' + f[0] + '" already exists in ' + _file_target)
    

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) == 4 or len(sys.argv) > 5:
        print('correct usage: python main.py <path> <min_epoch_time_in_sec> [<target> <modified_epoch_time_in_sec>]')
    else:
        _path = sys.argv[1]
        _min_time = float(sys.argv[2])
        _target = None
        _utime = None
        fl = []
        if len(sys.argv) == 5:
            _target = sys.argv[3]
            _utime = float(sys.argv[4])
        for f in getFileList(_path, lambda path: timeFilter(path, _min_time)):
            fl.append(getPath(f))
            statusMessage(f)
            if _target is not None:
                actionOnTarget(f, _path, _target, _utime)

        with open("output.txt", "w") as outfile:
            outfile.write("\n".join(fl))