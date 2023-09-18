#!/usr/bin/env python

import pandas as pd

FPATH_LOG = 'logs/Wellington/retinotopic-2023-09-17_19-45-37.log'
START_TIME = 24.8

def wedge_start_to_half(wedge_start):
    if 0 <= wedge_start and wedge_start < 180:
        return 'right'
    else:
        return 'left'

fpath_events = FPATH_LOG.replace('.log', '.tsv')
df_log = pd.read_csv(FPATH_LOG, sep='\t', header=None, names=['label', 'time', 'info'])

df_events = df_log.copy()
df_events['Onset'] = df_events['time'] + START_TIME
df_events['Duration'] = 0
df_events['Amplitude'] = 1
df_events['trial_type'] = df_events['label']

idx_rows_flash = (df_events['label'] == 'retinotopic')
df_events.loc[idx_rows_flash, 'trial_type'] = df_events.loc[idx_rows_flash, 'info'].apply(
    lambda s: wedge_start_to_half(eval(s)['wedge_start'])
)

df_events = df_events[['Onset', 'Duration', 'Amplitude', 'trial_type']]
df_events.to_csv(fpath_events, sep='\t', index=False, header=True)
