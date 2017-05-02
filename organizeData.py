import math as m
import pandas as pd

doAll = ['total_packets_a2b',
        'total_packets_b2a',
        'ack_pkts_sent_a2b',
        'ack_pkts_sent_b2a',
        'pure_acks_sent_a2b',
        'pure_acks_sent_b2a',
        'sack_pkts_sent_a2b',
        'sack_pkts_sent_b2a',
        'dsack_pkts_sent_a2b',
        'dsack_pkts_sent_b2a',
        'max_sack_blks/ack_a2b',
        'max_sack_blks/ack_b2a',
        'unique_bytes_sent_a2b',
        'unique_bytes_sent_b2a',
        'actual_data_pkts_a2b',
        'actual_data_pkts_b2a',
        'actual_data_bytes_a2b',
        'actual_data_bytes_b2a',
        'rexmt_data_pkts_a2b',
        'rexmt_data_pkts_b2a',
        'rexmt_data_bytes_a2b',
        'rexmt_data_bytes_b2a',
        'zwnd_probe_pkts_a2b',
        'zwnd_probe_pkts_b2a',
        'zwnd_probe_bytes_a2b',
        'zwnd_probe_bytes_b2a',
        'outoforder_pkts_a2b',
        'outoforder_pkts_b2a',
        'pushed_data_pkts_a2b',
        'pushed_data_pkts_b2a',
        'sacks_sent_a2b',
        'sacks_sent_b2a',
        'urgent_data_pkts_a2b',
        'urgent_data_pkts_b2a',
        'urgent_data_bytes_a2b',
        'urgent_data_bytes_b2a',
        'mss_requested_a2b',
        'mss_requested_b2a',
        'avg_win_adv_a2b',
        'avg_win_adv_b2a',
        'initial_window_bytes_a2b',
        'initial_window_bytes_b2a',
        'initial_window_pkts_a2b',
        'initial_window_pkts_a2b',
        'data_xmit_time_a2b',
        'data_xmit_time_b2a',
        'idletime_max_a2b',
        'idletime_max_b2a',
        'throughput_a2b',
        'throughput_b2a',
        'delta',
        'SYN_pkts_sent_a2b',
        'FIN_pkts_sent_a2b',
		'SYN_pkts_sent_b2a',
        'FIN_pkts_sent_b2a'
]

avgOnly = ['adv_wind_scale_a2b',
        'adv_wind_scale_b2a'
        ]


maxOnly = ['max_segm_size_a2b',
        'max_segm_size_b2a',
        'max_win_adv_a2b',
        'max_win_adv_b2a'
        ]
minOnly = ['min_segm_size_a2b',
        'min_segm_size_b2a',
        'min_win_adv_a2b',
        'min_win_adv_b2a',  
        ]

#Calculate the delta time
def getDeltaTime(initial, final):
    return m.fabs(final - initial)


# Condense the csv file so it is in proper order for scikitlearn
def cleanData(f,index):
    outputFile ="./Data/Clean/" + f + "/" +f+"%02d"%index+".csv"  #CSV File Name
    newCols = []
    rowData = []
    fb = pd.read_csv(outputFile,skipinitialspace=True)
    # Lists are 1 indexed so need to be changed so they are 0 indexed
    for index, row in fb.iterrows():
        first = row['first_packet']
        last = row['last_packet']
        final = getDeltaTime(first, last)
        fb['delta'] = final 

        values = row['SYN/FIN_pkts_sent_a2b'].split('/')
        fb['SYN_pkts_sent_a2b'] = values[0]
        fb['FIN_pkts_sent_a2b'] = values[1]
   
        values = row['SYN/FIN_pkts_sent_b2a'].split('/')
        fb['SYN_pkts_sent_b2a'] = values[0]
        fb['FIN_pkts_sent_b2a'] = values[1]

    # Do all Calculations on the do all array
    for item in doAll:
        newCols.append(item+"_sum")
        newCols.append(item+"_mean")
        newCols.append(item+"_max")
        newCols.append(item+"_min")

        rowData.append(fb[item].sum())
        rowData.append(fb[item].mean())
        rowData.append(fb[item].max())
        rowData.append(fb[item].min())
    
    # Do all Calculations that require only mean
    for item in avgOnly:
        newCols.append(item+"_mean")
        rowData.append(fb[item].mean())
    
    # Do all calculations that require only max
    for item in maxOnly:
        newCols.append(item+"_max")
        rowData.append(fb[item].max())
    
    # Do all calculations that require only min
    for item in minOnly:
        newCols.append(item+"_min")
        rowData.append(fb[item].min())


    return rowData, newCols




