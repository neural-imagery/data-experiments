#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sys
from datetime import datetime

fname = sys.argv[1] #'timestamps_run02.csv'
start_time = float(sys.argv[2])#10.0
print(f'fname: {fname}\nstart_time: {start_time}')
input('[Enter] to confirm')

fname_tsv = fname.replace('.csv','.tsv')
df_csv = pd.read_csv(fname,sep=',')

df_events = pd.DataFrame()

def timestamp_to_ctime(ts:str) -> float:
    dt = datetime.strptime(ts, '%m/%d/%Y, %I:%M:%S %p')
    timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    return timestamp

t0 = timestamp_to_ctime(df_csv['timestamp'][0])
onset = [start_time + timestamp_to_ctime(i) - t0 for i in df_csv['timestamp']]
trial_type = []
for clip,event in zip(df_csv['clipType'],df_csv['event']):
    trial_type.append(clip if event=='started' else 'rest')

df_events['Onset'] = onset
df_events['Duration'] = 0
df_events['Amplitude'] = 1
df_events['trial_type'] = trial_type
df_events.to_csv(fname_tsv,sep='\t',index=False,header=True)

print(f"Written to {fname_tsv}")
