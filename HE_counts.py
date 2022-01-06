import pandas as pd
import numpy as np
Car_factor = 0.5
LGV_factor = 0.5
df = pd.read_csv(r"C:\Projects\A259\SMV\Daily0.csv")
df.drop(['Time Interval', '0 - 10 mph', '11 - 15 mph', '16 - 20 mph', '21 - 25 mph',
       '26 - 30 mph', '31 - 35 mph', '36 - 40 mph', '41 - 45 mph',
       '46 - 50 mph', '51 - 55 mph', '56 - 60 mph', '61 - 70 mph',
       '71 - 80 mph', '80+ mph', 'Avg mph'], inplace = True, axis=1)
df.dropna(subset = ['0 - 520 cm'], inplace=True)
sites = df['Site Name'].unique()
site_rename = {'30360474':'212_10001', '30360473':'10001_212', '5751/1': '10006_10018', '5752/1':'10018_10006',
               '30360486':'10058_10057', '30360485':'10057_10058'}

arrays = [['General','General','General','General','General','General','General','Total','Total','Total','Total','Total','Total','Total','Total','Total','Total',
'Cars','Cars','Cars','Cars','Cars','Cars','Cars','Cars','Cars','Cars','LGV','LGV','LGV','LGV','LGV','LGV','LGV','LGV','LGV','LGV',
'OGV1','OGV1','OGV1','OGV1','OGV1','OGV1','OGV1','OGV1','OGV1','OGV1','OGV2','OGV2','OGV2','OGV2','OGV2','OGV2','OGV2','OGV2','OGV2','OGV2'],
['Site No', 'Survey Date', 'Name of the Junction', 'X', 'Y', 'A-Node',
       'B-Node', ' 08:00 -  09:00', ' 09:00 -  10:00', ' 10:00 -  11:00',
       ' 11:00 -  12:00', ' 12:00 -  13:00', ' 13:00 -  14:00',
       ' 14:00 -  15:00', ' 15:00 -  16:00', ' 16:00 -  17:00',
       ' 17:00 -  18:00',' 08:00 -  09:00', ' 09:00 -  10:00', ' 10:00 -  11:00',
       ' 11:00 -  12:00', ' 12:00 -  13:00', ' 13:00 -  14:00',
       ' 14:00 -  15:00', ' 15:00 -  16:00', ' 16:00 -  17:00',
       ' 17:00 -  18:00',' 08:00 -  09:00', ' 09:00 -  10:00', ' 10:00 -  11:00',
       ' 11:00 -  12:00', ' 12:00 -  13:00', ' 13:00 -  14:00',
       ' 14:00 -  15:00', ' 15:00 -  16:00', ' 16:00 -  17:00',
       ' 17:00 -  18:00',' 08:00 -  09:00', ' 09:00 -  10:00', ' 10:00 -  11:00',
       ' 11:00 -  12:00', ' 12:00 -  13:00', ' 13:00 -  14:00',
       ' 14:00 -  15:00', ' 15:00 -  16:00', ' 16:00 -  17:00',
       ' 17:00 -  18:00', ' 08:00 -  09:00', ' 09:00 -  10:00', ' 10:00 -  11:00',
       ' 11:00 -  12:00', ' 12:00 -  13:00', ' 13:00 -  14:00',
       ' 14:00 -  15:00', ' 15:00 -  16:00', ' 16:00 -  17:00', ' 17:00 -  18:00']]

tuples = list(zip(*arrays))
columns = pd.MultiIndex.from_tuples(tuples, names=["first", "second"])
HE_counts = pd.DataFrame(np.empty([6,57]), columns = columns)
n=0
for site in sites:
    counts = df.where(df['Site Name']==site)
    counts['day'] = counts.loc[:,'Report Date'].str[:2]
    counts['hour'] = counts.loc[:,'Time Period Ending'].str[:2]
    counts = counts[counts['Total Volume']!=0]
    weekdays = counts[counts['day'].isin(['01','04', '05', '06','07',
                                      '08','11', '12', '13', '14','15',
                                      '18', '19', '20', '21','22', '25',
                                      '28','29'])]
    weekdays = weekdays.groupby(['day','hour']).sum()
    export = weekdays.groupby('hour').mean()
    export.to_csv(r'C:\Projects\A259\SMV\HE' +site_rename[site] + '.csv')
    HE_counts.iloc[n,0] = site
    HE_counts.iloc[n,1] = 'Mar_2019'
    HE_counts.iloc[n,5] = site_rename[site].split('_')[0]
    HE_counts.iloc[n,6] = site_rename[site].split('_')[1]
    HE_counts.loc[n,('Total',' 08:00 -  09:00')] = export.loc['08','Total Volume']
    HE_counts.loc[n,('Total',' 09:00 -  10:00')] = export.loc['09','Total Volume']
    HE_counts.loc[n,('Total',' 10:00 -  11:00')] = export.loc['10','Total Volume']
    HE_counts.loc[n,('Total',' 11:00 -  12:00')] = export.loc['11','Total Volume']
    HE_counts.loc[n,('Total',' 12:00 -  13:00')] = export.loc['12','Total Volume']
    HE_counts.loc[n,('Total',' 13:00 -  14:00')] = export.loc['13','Total Volume']
    HE_counts.loc[n,('Total',' 14:00 -  15:00')] = export.loc['14','Total Volume']
    HE_counts.loc[n,('Total',' 15:00 -  16:00')] = export.loc['15','Total Volume']
    HE_counts.loc[n,('Total',' 16:00 -  17:00')] = export.loc['16','Total Volume']
    HE_counts.loc[n,('Total',' 17:00 -  18:00')] = export.loc['17','Total Volume']
    HE_counts.loc[n,('Cars',' 08:00 -  09:00')] = export.loc['08','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('Cars',' 09:00 -  10:00')] = export.loc['09','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('Cars',' 10:00 -  11:00')] = export.loc['10','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('Cars',' 11:00 -  12:00')] = export.loc['11','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('Cars',' 12:00 -  13:00')] = export.loc['12','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('Cars',' 13:00 -  14:00')] = export.loc['13','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('Cars',' 14:00 -  15:00')] = export.loc['14','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('Cars',' 15:00 -  16:00')] = export.loc['15','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('Cars',' 16:00 -  17:00')] = export.loc['16','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('Cars',' 17:00 -  18:00')] = export.loc['17','0 - 520 cm'] * Car_factor
    HE_counts.loc[n,('LGV',' 08:00 -  09:00')] = export.loc['08','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('LGV',' 09:00 -  10:00')] = export.loc['09','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('LGV',' 10:00 -  11:00')] = export.loc['10','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('LGV',' 11:00 -  12:00')] = export.loc['11','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('LGV',' 12:00 -  13:00')] = export.loc['12','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('LGV',' 13:00 -  14:00')] = export.loc['13','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('LGV',' 14:00 -  15:00')] = export.loc['14','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('LGV',' 15:00 -  16:00')] = export.loc['15','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('LGV',' 16:00 -  17:00')] = export.loc['16','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('LGV',' 17:00 -  18:00')] = export.loc['17','0 - 520 cm'] * LGV_factor
    HE_counts.loc[n,('OGV1',' 08:00 -  09:00')] = export.loc['08','521  - 660 cm']
    HE_counts.loc[n,('OGV1',' 09:00 -  10:00')] = export.loc['09','521  - 660 cm']
    HE_counts.loc[n,('OGV1',' 10:00 -  11:00')] = export.loc['10','521  - 660 cm']
    HE_counts.loc[n,('OGV1',' 11:00 -  12:00')] = export.loc['11','521  - 660 cm']
    HE_counts.loc[n,('OGV1',' 12:00 -  13:00')] = export.loc['12','521  - 660 cm']
    HE_counts.loc[n,('OGV1',' 13:00 -  14:00')] = export.loc['13','521  - 660 cm']
    HE_counts.loc[n,('OGV1',' 14:00 -  15:00')] = export.loc['14','521  - 660 cm']
    HE_counts.loc[n,('OGV1',' 15:00 -  16:00')] = export.loc['15','521  - 660 cm']
    HE_counts.loc[n,('OGV1',' 16:00 -  17:00')] = export.loc['16','521  - 660 cm']
    HE_counts.loc[n,('OGV1',' 17:00 -  18:00')] = export.loc['17','521  - 660 cm']
    HE_counts.loc[n,('OGV2',' 08:00 -  09:00')] = export.loc['08','661 - 1160 cm'] + export.loc['08','1160+ cm']
    HE_counts.loc[n,('OGV2',' 09:00 -  10:00')] = export.loc['09','661 - 1160 cm'] + export.loc['09','1160+ cm']
    HE_counts.loc[n,('OGV2',' 10:00 -  11:00')] = export.loc['10','661 - 1160 cm'] + export.loc['10','1160+ cm']
    HE_counts.loc[n,('OGV2',' 11:00 -  12:00')] = export.loc['11','661 - 1160 cm'] + export.loc['11','1160+ cm']
    HE_counts.loc[n,('OGV2',' 12:00 -  13:00')] = export.loc['12','661 - 1160 cm'] + export.loc['12','1160+ cm']
    HE_counts.loc[n,('OGV2',' 13:00 -  14:00')] = export.loc['13','661 - 1160 cm'] + export.loc['13','1160+ cm']
    HE_counts.loc[n,('OGV2',' 14:00 -  15:00')] = export.loc['14','661 - 1160 cm'] + export.loc['14','1160+ cm']
    HE_counts.loc[n,('OGV2',' 15:00 -  16:00')] = export.loc['15','661 - 1160 cm'] + export.loc['15','1160+ cm']
    HE_counts.loc[n,('OGV2',' 16:00 -  17:00')] = export.loc['16','661 - 1160 cm'] + export.loc['16','1160+ cm']
    HE_counts.loc[n,('OGV2',' 17:00 -  18:00')] = export.loc['17','661 - 1160 cm'] + export.loc['17','1160+ cm']
    n+=1
    