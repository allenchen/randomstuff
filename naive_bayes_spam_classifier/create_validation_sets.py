import os
import shutil
import random

def get_files(path):
    for f in os.listdir(path):
        f = os.path.abspath( os.path.join(path, f ) )
        if os.path.isfile( f ):
            yield f

# Ham
x = 1
for filename in get_files("train/ham"):
    print "Placed " + str(filename)
    shutil.copyfile(filename, "xvalidation/ham/" + str(random.randint(1,10)) + "/" + str(x) + ".txt")
    x += 1

# Spam
x = 1
for filename in get_files("train/spam"):
    print "Placed " + str(filename)
    shutil.copyfile(filename, "xvalidation/spam/" + str(random.randint(1,10)) + "/" + str(x) + ".txt")
    x += 1
