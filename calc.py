from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

outputDir = "output/"
RegressionReport = outputDir + "RegressionReport.csv"
RegressionMean = outputDir + "RegressionMean.csv"

report_df = pd.read_csv(RegressionReport, index_col=0)
rmean_df = pd.read_csv(RegressionMean)
# get 'intercept' property:
# print(rmean_df.iloc[1][1])

# get 'coef' property:
std_coef = rmean_df.iloc[0][1]
std_intercept = rmean_df.iloc[1][1]

# build tag list
# ref_entry = 44 <==> 24 Celsius
ENTRY = 44
tag_list = report_df['tag_id']

# add column 'coef_diff': coef diff with regression mean coef
calc_df = report_df
#calc_df['coef_diff'] = calc_df['coef']
#calc_df['coef_diff'] = calc_df['coef_diff'].map(lambda coef: coef - std_coef)
#print(calc_df)

# get report temperature on real -20

tag_report_on_minus_20 = list()
for tag_id in tag_list:
    tag_mean = pd.read_csv(outputDir + tag_id + '_mean.csv')
    tag_report_on_minus_20.append( tag_mean.iloc[ 0 ]['curTemp'] )

calc_df['minus_20'] = tag_report_on_minus_20
calc_df['minus_20'] = calc_df['minus_20'] - (-20)

print(calc_df)
calc_df.to_csv(outputDir + 'error_on_minus_20.csv')
