from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np

df = pd.DataFrame()
summary = list()
myPath = "Temperature_Data"
fileList = [f for f in listdir(myPath) if isfile(join(myPath, f))]


# Read line by line, append each line with target temperature
# put them in pandas DataFrame

for fname in fileList:
    f = open(join(myPath, fname))
    while True:
        line = f.readline()
        if line:
            x = line.split()
            x.append(fname)
            summary.append(x)
        else:
            break
    f.close()
df=pd.DataFrame(summary, columns=["day", "time", "tid", "base", "refADC", "curADC", "curTemp", "tempUT"])
print(df)
