import pandas as pd
import numpy as np

am=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/Base_2018_Hwy_TS1_i8c_I6_AM.csv', names=list(range(1,2771)))
ip=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/Base_2018_Hwy_TS2_i8c_I6_IP.csv', names=list(range(1,2771)))
pm=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/Base_2018_Hwy_TS3_i8c_I6_PM.csv', names=list(range(1,2771)))

outside = list()
inside = list()

for i in ('L1', 'L2', 'L3', 'L4', 'HGV'):
    for j in range(1,2771):
        outside.append(i)
        inside.append(j)
        
indices = list(zip(outside, inside))
indices = pd.MultiIndex.from_tuples(indices)

am.index = indices
ip.index = indices
pm.index = indices

am_lgv = pd.DataFrame(np.empty([2770,2770]),index=list(range(1,2771)),columns=list(range(1,2771)))
for i in range(2770):
    am_lgv.iloc[i]=am.iloc[i]+am.iloc[i+2770]+am.iloc[i+2770*2]+am.iloc[i+2770*3]
ip_lgv = pd.DataFrame(np.empty([2770,2770]),index=list(range(1,2771)),columns=list(range(1,2771)))
for i in range(2770):
    ip_lgv.iloc[i]=ip.iloc[i]+ip.iloc[i+2770]+ip.iloc[i+2770*2]+ip.iloc[i+2770*3]
pm_lgv = pd.DataFrame(np.empty([2770,2770]),index=list(range(1,2771)),columns=list(range(1,2771)))
for i in range(2770):
    pm_lgv.iloc[i]=pm.iloc[i]+pm.iloc[i+2770]+pm.iloc[i+2770*2]+pm.iloc[i+2770*3]
    
am=pd.concat([am,am_lgv])
ip=pd.concat([ip,ip_lgv])
pm=pd.concat([pm,pm_lgv])

outside = list()
inside = list()

for i in ('L1', 'L2', 'L3', 'L4', 'HGV', 'LGV'):
    for j in range(1,2771):
        outside.append(i)
        inside.append(j)
        
indices = list(zip(outside, inside))
indices = pd.MultiIndex.from_tuples(indices)

am.index=indices
ip.index=indices
pm.index=indices

clusters = pd.read_csv('C:/Users/ukiws001/Desktop/East Riding QGIS/North_Zones_v2.10/noham_zones_freeze_2.10.dbf.csv')
clusters.index = list(range(1,2771))
zones = pd.DataFrame(clusters['Cluster'], index=indices)

for i in ('L1', 'L2', 'L3', 'L4', 'HGV', 'LGV'):
    for j in range(1,2771):
        zones.loc[(i,j), 'Cluster'] = clusters.loc[j, 'Cluster']

am['sum'] = am[1]
for k in range(2770*6):
    am.iloc[k,2770] = am.iloc[k, 0:2770].sum()
am_v2=pd.concat([am['sum'],zones],axis=1)
    
ip['sum'] = am[1]
for k in range(2770*6):
    ip.iloc[k,2770] = ip.iloc[k, 0:2770].sum()
ip_v2=pd.concat([am['sum'],zones],axis=1)
    
pm['sum'] = pm[1]
for k in range(2770*6):
    pm.iloc[k,2770] = pm.iloc[k, 0:2770].sum()
pm_v2=pd.concat([pm['sum'],zones],axis=1)

L1 = am_v2.loc['L1'].groupby('Cluster').sum()
L2 = am_v2.loc['L2'].groupby('Cluster').sum()
L3 = am_v2.loc['L3'].groupby('Cluster').sum()
L4 = am_v2.loc['L4'].groupby('Cluster').sum()
LGV = am_v2.loc['LGV'].groupby('Cluster').sum()
HGV = am_v2.loc['HGV'].groupby('Cluster').sum()
    
am_final = pd.DataFrame(np.empty([22,6]), index = L1.index, columns = ['L1','L2','L3','L4','HGV','LGV'])

am_final['L1'] = L1
am_final['L2'] = L2
am_final['L3'] = L3
am_final['L4'] = L4
am_final['LGV'] = LGV
am_final['HGV'] = HGV

L1 = ip_v2.loc['L1'].groupby('Cluster').sum()
L2 = ip_v2.loc['L2'].groupby('Cluster').sum()
L3 = ip_v2.loc['L3'].groupby('Cluster').sum()
L4 = ip_v2.loc['L4'].groupby('Cluster').sum()
LGV = ip_v2.loc['LGV'].groupby('Cluster').sum()
HGV = ip_v2.loc['HGV'].groupby('Cluster').sum()
    
ip_final = pd.DataFrame(np.empty([22,6]), index = L1.index, columns = ['L1','L2','L3','L4','HGV','LGV'])

ip_final['L1'] = L1
ip_final['L2'] = L2
ip_final['L3'] = L3
ip_final['L4'] = L4
ip_final['LGV'] = LGV
ip_final['HGV'] = HGV

L1 = pm_v2.loc['L1'].groupby('Cluster').sum()
L2 = pm_v2.loc['L2'].groupby('Cluster').sum()
L3 = pm_v2.loc['L3'].groupby('Cluster').sum()
L4 = pm_v2.loc['L4'].groupby('Cluster').sum()
LGV = pm_v2.loc['LGV'].groupby('Cluster').sum()
HGV = pm_v2.loc['HGV'].groupby('Cluster').sum()
    
pm_final = pd.DataFrame(np.empty([22,6]), index = L1.index, columns = ['L1','L2','L3','L4','HGV','LGV'])

pm_final['L1'] = L1
pm_final['L2'] = L2
pm_final['L3'] = L3
pm_final['L4'] = L4
pm_final['LGV'] = LGV
pm_final['HGV'] = HGV

am_final.to_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_am2.csv')
ip_final.to_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_ip2.csv')
pm_final.to_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_pm2.csv')

