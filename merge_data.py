from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




# Read line by line, append each line with target temperature
# put them in pandas DataFrame and return


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

    df = pd.DataFrame(summary, columns=["day", "time", "tagID", "adcBase", "refADC", "curADC", "curTemp", "tempUT"])
    numeric_cols = ["adcBase", "refADC", "curADC", "curTemp", "tempUT"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce', axis=1)
    df.sort_values(by=['tagID', 'curTemp', "day", "time"], inplace=True)
    return df




# split_tempUT()
# return a dict of partitioned tempUT
# input: dataframe of a tag ID
# output: dict of a tag, key is temperature, value is
#         the related dataframe

def split_tempUT(df):
    # build 'temperature under test' list of a tag
    tempUT = df["tempUT"].unique().tolist()
    d = dict()
    for t in tempUT:
        # select temperature from dataframe
        oneTemp = df[df["tempUT"] == t]
        #print(oneTemp)
        d[t] = oneTemp
    return d


# get_means(df)
# input dataframe of a tag_id on a single temperature UT
# output a series with means of 'curADC' and 'curTemp' index
# like:
#         base         23.000000
#         refADC     1301.000000
#         curADC     1369.666667
#         curTemp     379.333333
#         tempUT       40.100000

def get_means(df):
    temp_list = df[1:4]
    m = temp_list.mean()
    #print("mean = {}, meanADC = {}, meanTemp ={}".format(m, m['curADC'], m['curTemp']))
    return m



def process_one_tag(tag_id, one_tag_df):
    enable_second_y_axis = False
    d = split_tempUT(one_tag_df)

    tempUT_list = list()
    temp_list = list()
    adc_list = list()

    for key in list(d.keys()):
        tag_means = get_means(d[key])
        #print("tUT = {}, tMean = {}".format(key, f))
        temp_list.append(tag_means['curTemp']/10)
        tempUT_list.append(float(key))
        adc_list.append(tag_means['curADC'])

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Temperature Under Test')
    ax1.set_ylabel('ADC', color=color)  # we already handled the x-label with ax1
    ax1.plot(tempUT_list, adc_list, 'r.')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(axis='both', which='both')

    # plot 2 y axises on one x axis (temperature)
    if enable_second_y_axis:
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel('Real Temperature', color=color)
        ax2.plot(tempUT_list, temp_list, 'b+')
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.grid(color=color, axis='y', which='both')

    plt.title(tag_id)
    plt.savefig("output/" + tag_id + ".eps", format = 'eps')
    plt.clf()





df = build_data_frame()
print(df)

# build tag list
tagID = df["tagID"].unique().tolist()

# iterate tag list
for tag_id in tagID:
    # select from dataframe of each tag ID
    one_tag_df = df[ df["tagID"] == tag_id ]
    process_one_tag(tag_id, one_tag_df)
