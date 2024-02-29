#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 09:48:15 2023

@author: hcliffo
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt

today = datetime.date.today()

data = pd.read_csv('ve_ur_downloads_22924.csv')

# clean dataset
data['Date'] = data['time_micros'].apply(lambda x:  datetime.datetime.fromtimestamp(x/1000000).strftime('%m-%d-%Y'))
data_download = data[data['cs_method']=='GET']
data_download = data_download[data_download['cs_object'].notnull()]
data_download = data_download[~data_download['cs_user_agent'].isna()]

# removes facebook and slack bots
data_download = data_download[~data_download['cs_user_agent'].str.startswith(('facebook', 'Slack'))]

# remove heather's downloads
data_download = data_download[~data_download['c_ip'].isin(['2403:6b80:8:100::6773:a52'])]

#sort values by date
data_download = data_download.sort_values(by='Date',ascending=False)


# get the type of resource and the file name from the cs_object column
types =[]
files = []
for i in data_download['cs_object']:
    types.append(i.split('/')[0])
    files.append(i.split('/')[1])
    
data_download['Type'] = types
data_download['File'] = files 


# only select the following columns to keep
data_download = data_download[[ 'Type', 'File','Date']]

# create group by of date and type by count
downloads = data_download.groupby(['Date','Type']).count().reset_index()
downloads = downloads.pivot(index='Date', columns='Type')
downloads.columns = downloads.columns.droplevel(0)

#sort by date
dates = downloads.index.tolist()
dates.sort(key = lambda date: datetime.datetime.strptime(date, '%m-%d-%Y'))
df_dl = downloads.reindex(dates)

#create figure
fig,ax = plt.subplots(figsize=(15,6))
df_dl.plot(kind='bar',stacked=True,ax=ax)
ax.set_ylabel('# of Downloads')
ax.set_xlabel('Date')
ax.xaxis.set_major_locator(plt.MaxNLocator(int(len(downloads)/2)))
plt.tight_layout()
fig.savefig('ve_database_downloads_{}_bar.png'.format(today))

#create figure
fig,ax = plt.subplots(figsize=(15,6))
df_dl.plot(ax=ax)
ax.set_ylabel('# of Downloads')
ax.set_xlabel('Date')
ax.xaxis.set_major_locator(plt.MaxNLocator(int(len(downloads)/2)))
plt.tight_layout()
fig.savefig('ve_database_downloads_{}_line.png'.format(today))
