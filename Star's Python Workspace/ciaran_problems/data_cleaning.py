import os

path = '/Users/quanyewu/Desktop/files/lsi'
list_dirs = os.walk(path)
for root, dirs, files in list_dirs:
    for file in files:
        fsize = os.path.getsize(path + '/' + file)
        if fsize < 1000:
            os.remove(path + '/' + file)
