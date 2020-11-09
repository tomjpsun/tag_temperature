from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

outputDir = "output/"
RegressionReport = outputDir + "RegressionReport.txt"

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
    # change strings to numeric values
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

    # save to csv before plotting
    mean_df = pd.DataFrame( {
        'tempUT': tempUT_list,
        'curADC': adc_list,
        'curTemp': temp_list } )

    mean_df.to_csv(outputDir + tag_id + '_mean.csv', index=False)


    # plot
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
    plt.savefig(outputDir + tag_id + ".pdf", format = 'pdf')
    plt.close()



def regression_report(tagList):
    print(RegressionReport)
    with open(RegressionReport, 'w') as f:
        for tag_id in tagList:
            df = pd.read_csv(outputDir + tag_id + '_mean.csv')
            reg = linear_model.LinearRegression()
            reg.fit(df[['tempUT']], df['curADC'])
            f.write('tag {}: co {}, intr {}\n'.format(tag_id, reg.coef_, reg.intercept_))



def plot_all(tagList):
    legends = list()
    # set plot size (such that legend won't block the drawed line)
    plt.rcParams["figure.figsize"] = (10,10)
    # drop out 1st tag: 0201000001 since it has no data
    for tag_id in tagList[1:]:
        # read mean data for each tag
        df = pd.read_csv(outputDir + tag_id + '_mean.csv')
        # plot each tag, and collect its legend
        legend, = plt.plot(df['tempUT'].tolist(), df['curADC'].tolist(), label=tag_id)
        legends.append(legend)

    plt.xticks(np.arange(-20, 50, step=5))
    plt.yticks(np.arange(1000, 1500, step=25))
    plt.xlabel('Temperature Under Test')
    plt.ylabel('ADC')
    plt.grid(axis='both', which='both')
    plt.title('All Tags')
    plt.legend(handles=legends)

    plt.savefig(outputDir + 'all_tags.pdf', format='pdf')
    plt.close()



df = build_data_frame()
# print(df)

# build tag list
tagList = df["tagID"].unique().tolist()
print(tagList)

# iterate tag list
for tag_id in tagList:
    # select from dataframe of each tag ID
    one_tag_df = df[ df["tagID"] == tag_id ]

    # process each tag, save to csv by the way
    one_tag_df.to_csv(outputDir + tag_id + '_raw.csv', index=False)
    process_one_tag(tag_id, one_tag_df)

# regression report
regression_report(tagList)

# plot all together
print('plot_all()\n')
plot_all(tagList)
