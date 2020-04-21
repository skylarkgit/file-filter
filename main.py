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
            try:
                if filter is None or filter(r): 
                    fArr.append([r, None, None])
                    isDirectoryTraversed = True
            except:
                fArr.append([None, r, None])
                isDirectoryTraversed = True
        if isDirectoryTraversed is False:
            for i in f:
                try:
                    if filter is None or filter(os.path.join(r,i)):
                        fArr.append([r, i, None])
                except:
                    fArr.append([None, r, i])
    return fArr

def getPath(f):
    if f[1] is not None:
        _file_src = os.path.join(f[0], f[1])
    else:
        _file_src = f[0]
    return _file_src

def statusMessage(f):
    if f[0] is None:
        if len(f) > 2:
            print('error: file: ' + getPath(f[1:3]))
        else:
            print('error: folder: ' + getPath(f[1:3]))
    elif f[1] is not None:
        print('file: ' + os.path.join(f[0], f[1]))
    else:
        print('folder: ' + f[0])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('correct usage: python main.py <path> <min_epoch_time_in_sec>')
    else:
        _path = sys.argv[1]
        _min_time = float(sys.argv[2])
        fl = []
        efl = []    # error array
        for f in getFileList(_path, lambda path: timeFilter(path, _min_time)):
            if f[0] is not None:
                fl.append(getPath(f))
            else:
                efl.append(getPath(f[1:3]))
            statusMessage(f)

        with open("output.txt", "w") as outfile:
            outfile.write("\n".join(fl))
        with open("error-output.txt", "w") as outfile:
            outfile.write("\n".join(efl))