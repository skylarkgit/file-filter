import os
import time

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

for f in getFileList('/home/abhay-verma/temp/tcs/sample-root', lambda path: timeFilter(path, 1587139722)):
    print('file "' + f[1] + '" in "' + f[0] + '" has changed recently')