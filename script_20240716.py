# -*- coding: utf-8 -*-
"""
Author: Jason Welsh
Description: file computes the differences and percent differences of files within a designated directory.  It also
takes the binv command from linux and computes the differences for all the categories and produces a difference
and percent difference as well.
Date Updated: July 10, 2024
"""
import numpy as np
import os
import pandas as pd
import subprocess

limiter = "t00z"

dir1 = "/lfs/h2/emc/ptmp/ashley.stanfield/CRON/urma_v13/com/obsproc/v1.3/urma.20240829"

dir2 = "/lfs/h2/emc/ptmp/ashley.stanfield/CRON/3d_urma.12/com/obsproc/v1.2/urma.20240829" 

prepbufr1 = dir1 + "/" + "urma." +limiter+ ".prepbufr.tm00"

prepbufr2 = dir2 + "/" + "urma."+limiter+".prepbufr.tm00"

binv = "/u/ashley.stanfield/bin/binv"

#specify where to find the STMP and COMROOT directories
#mySTMP = '/scratch1/NCEPDEV/global/glopara/dump/gdas.20240720/00/atmos/' #'C:/Users/jason.welsh/Downloads'
#STMP = subprocess.call('"$STMP"',shell=False)
#myCOMROOT = '/scratch1/NCEPDEV/global/glopara/dump/gdas.20240720/00/atmos/' #'C:/Users/jason.welsh/Downloads'
#COMROOT = subprocess.call('"$COMROOT"',shell=False)

#place the STMP path into a thePath variable
thePath_in = dir1
thePath_out = dir2

#list the complete directory of where PREFIX files are located in the "in" directory
prefix_in = "bufr_d"
theFiles_in = [filename for filename in os.listdir('.') if filename.startswith(prefix_in)]

#list the complete directory of where the files are located for a specific hour
prefix_in = "00"
theFiles_in = [theFiles_in for theFiles_in in os.listdir('.') if theFiles_in.startswith(prefix_in)]

#list the complete directory of where ALL the files are located in the "in" directory
theFiles_in = list(os.listdir(thePath_in))

#place all the file names into a variable called 'filen'_in (file name) to be used later
filess_in = []
filen_in = []
for i in range(len(theFiles_in)):
    fileSize = os.path.getsize(thePath_in+'/'+theFiles_in[i])
    filess_in.append(fileSize)
    filen_in.append(theFiles_in[i])
    
#list the complete directory of where PREFIX files are located in the "out" directory
thePath_out = dir2
prefix_out = "bufr_d"
theFiles_out = [filename for filename in os.listdir('.') if filename.startswith(prefix_out)]
#list the complete directory of where ALL the files are located in the "out" directory
theFiles_out = list(os.listdir(thePath_out))

#place all the file names into a variable called 'filess'_out (files size) to be used later
filess_out = []
filen_out = []
for i in range(len(theFiles_out)):
    fileSize = os.path.getsize(thePath_out+'/'+theFiles_out[i])
    filess_out.append(fileSize)
    filen_out.append(theFiles_out[i])

#place the variables from filen and filess from the input and output file directories into dataframes
filess_in = pd.DataFrame(filess_in)
filess_out = pd.DataFrame(filess_out)

filen_in = pd.DataFrame(filen_in)
filen_out = pd.DataFrame(filen_out)

#Compute only the values that are equal between each directory for differences and percent differences

equal_names_only_in = filen_in[filen_in == filen_out]

equal_values_only_in = filess_in[filen_in == filen_out]

equal_names_only_out = filen_out[filen_in == filen_out]

equal_values_only_out = filess_out[filen_in == filen_out]

diff_file_sizes = equal_values_only_in - equal_values_only_out

percent_diff = diff_file_sizes/equal_values_only_out

#Place computed values into a table and save to a csv file
table_of_diff_percent_diff = pd.concat([equal_names_only_in, equal_values_only_in, equal_names_only_out, equal_values_only_out, diff_file_sizes, percent_diff], axis=1)

table_of_diff_percent_diff.columns = ['Names', 'Sizes', 'Names', 'Sizes', 'Diff', '% Diff']

table_of_diff_percent_diff.sort_values('Names', ascending=True)

table_of_diff_percent_diff.to_csv('table_of_diff_percent_diff.csv')

#Place your own path names to where you would like to compare the two prepbufr files
os.system(binv prepbufr1  " > output1.csv")
os.system(binv prepbufr2  " > output2.csv")

#After writing out the two csv files from the binv command; read the files into be processed further
output1 = pd.read_csv("output1.csv")
output2 = pd.read_csv("output2.csv")

#Convert a string to a list from output1 and output2

def Convert(string):
    li = list(string.split(" "))
    return li

def strip(array):
    result = []
    for ele in array:
        if ele.strip():
            result.append(ele)
    return result

OUTPUT1 = [[]]
i = 0
while "TOTAL" not in output1.iat[i,0]:
    OUTPUT1.append(strip(Convert(output1.iat[i,0])))
    i = i + 1

OUTPUT1.append(strip(Convert(output1.iat[i,0])))

OUTPUT2 = [[]]
i = 0
while "TOTAL" not in output2.iat[i,0]:
    OUTPUT2.append(strip(Convert(output2.iat[i,0])))
    i = i + 1

OUTPUT2.append(strip(Convert(output2.iat[i,0])))

y_d = np.shape(OUTPUT1)

table = np.zeros((4,y_d[0]-1))

output_subset1 = []
output_subset2 = []
names = []

for v in range(3):
    for c in range(y_d[0]-1):
        table[v,c]=float(OUTPUT1[c+1][v+1]) - float(OUTPUT2[c+1][v+1])
        names.append(OUTPUT1[c+1][v])
        


ppd1 = np.zeros((1,y_d[0]-1))
ppd2 = np.zeros((1,y_d[0]-1))

for vv in range(0):
    for c in range(y_d[0]-1):
        ppd1[v,c]=float(table[c+1][vv+2])/float(OUTPUT1[c+1][vv+2])
        ppd2[v,c]=float(table[c+1][vv+2])/float(OUTPUT2[c+1][vv+2])
        




table = pd.DataFrame(table)
ppd1 = pd.DataFrame(ppd1)
ppd2 = pd.DataFrame(ppd2)


names=names[0:y_d[0]-3]
names.append("TOTAL")

names = pd.DataFrame(names)

names = pd.DataFrame(names)

table111 = pd.concat([names, table.T,ppd1.T,ppd2.T], axis=1)

table111.columns = ['Type', 'messages', 'subsets', 'bytes', 'unamed', 'percent prepbufr diff output1','percent prepbufr diff output2']
table111 = table111.iloc[:-1]
table111.to_csv('table_of_diff.csv')
