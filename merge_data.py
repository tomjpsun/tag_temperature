from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np



# Read line by line, append each line with target temperature
# put them in pandas DataFrame

def build_data_frame():
    df = pd.DataFrame()
    summary = list()
    myPath = "Temperature_Data"
    fileList = [f for f in listdir(myPath) if isfile(join(myPath, f))]

    for fname in fileList:
        f = open(join(myPath, fname))
        while True:
            line = f.readline()
            if line:
                x = line.split()
                x.append(fname) # append target temperature
                summary.append(x) # summary is a list of list
            else:
                break
        f.close()
    df=pd.DataFrame(summary, columns=["day", "time", "tagID", "base", "refADC", "curADC", "curTemp", "tempUT"])
    return df


def draw_tag(tag_id, df):
    oneTag = df[df["tagID"] == tag_id]
    print(oneTag)


# return a list of partitioned tempUT
def split_tempUT(df):
    # build tempUT list
    tempUT = df["tempUT"].unique().tolist()
    final_list = list()
    for t in tempUT:
        # select temperature from dataframe
        oneTemp = df[df["tempUT"] == t]
        print(oneTemp)
        final_list.append(oneTemp)
    return final_list


df = build_data_frame()
tagID = df["tagID"].unique().tolist()

# select a tag
one_tag_df = df[df["tagID"] == tagID[0]]
split_tempUT(one_tag_df)

#draw_tag('8680000006', df)
