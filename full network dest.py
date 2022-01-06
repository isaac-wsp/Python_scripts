import pandas as pd
import numpy as np

clusters = pd.read_csv('C:/Users/ukiws001/Desktop/East Riding QGIS/North_Zones_v2.10/noham_zones_freeze_2.10.dbf.csv')
clusters.index = list(range(1,2771))

for i,j in zip(['TS1','TS2','TS3'],['AM','IP','PM']):
    df=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/Base_2018_Hwy_'+i+'_i8c_I6_'+j+'.csv',names=list(range(1,2771)))
    outside = list()
    inside = list()

    for k in ('L1', 'L2', 'L3', 'L4', 'HGV'):
        for l in range(1,2771):
            outside.append(k)
            inside.append(l)
        
    indices = list(zip(outside, inside))
    indices = pd.MultiIndex.from_tuples(indices)
    df.index=indices
    df_lgv = pd.DataFrame(np.empty([2770,2770]),index=list(range(1,2771)),columns=list(range(1,2771)))
    for k in range(2770):
        df_lgv.iloc[k]=df.iloc[k]+df.iloc[k+2770]+df.iloc[k+2770*2]+df.iloc[k+2770*3]
    df=pd.concat([df,df_lgv])
    outside = list()
    inside = list()

    for k in ('L1', 'L2', 'L3', 'L4', 'HGV', 'LGV'):
        for l in range(1,2771):
            outside.append(k)
            inside.append(l)
        
    indices = list(zip(outside, inside))
    indices = pd.MultiIndex.from_tuples(indices)

    df.index=indices
    
    L1 = df.loc['L1'].transpose()
    L2 = df.loc['L2'].transpose()
    L3 = df.loc['L3'].transpose()
    L4 = df.loc['L4'].transpose()
    LGV = df.loc['LGV'].transpose()
    HGV = df.loc['HGV'].transpose()
        
    L1['sum'] = L1[1]
    L2['sum'] = L2[1]
    L3['sum'] = L3[1]
    L4['sum'] = L4[1]
    LGV['sum'] = LGV[1]
    HGV['sum'] = HGV[1]
        
    for l in range(2770):
        L1.iloc[l,2770]=L1.iloc[l,0:2770].sum()
        L2.iloc[l,2770]=L2.iloc[l,0:2770].sum()
        L3.iloc[l,2770]=L3.iloc[l,0:2770].sum()
        L4.iloc[l,2770]=L4.iloc[l,0:2770].sum()
        LGV.iloc[l,2770]=LGV.iloc[l,0:2770].sum()
        HGV.iloc[l,2770]=HGV.iloc[l,0:2770].sum()
        
    L1.index=clusters.index
    L2.index=clusters.index
    L3.index=clusters.index
    L4.index=clusters.index
    LGV.index=clusters.index
    HGV.index=clusters.index
        
    L1 = pd.concat([L1['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
    L2 = pd.concat([L2['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
    L3 = pd.concat([L3['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
    L4 = pd.concat([L4['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
    LGV = pd.concat([LGV['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
    HGV = pd.concat([HGV['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
    
    Final = pd.DataFrame(np.empty([22,6]), index = L1.index, columns = ['L1','L2','L3','L4','HGV','LGV'])
        
    Final['L1'] = L1
    Final['L2'] = L2
    Final['L3'] = L3
    Final['L4'] = L4
    Final['LGV'] = LGV
    Final['HGV'] = HGV
    Final.to_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_dest'+j+'2.csv')
