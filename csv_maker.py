#FIRST FILE, CREATES LARGE CSVS OF ALL TRIPS BETWEEN ALL ZONES ALONG EACH LINK

import pandas as pd
import numpy as np


links = ['_70280_72899_', '_72899_70280_','_70252_73545_','_73545_70252_','_70385_74627_', '_74627_70385_','_78002_70260_','_70260_78002_']

for i in links:
    for j in ['\AM','\IP','\PM']:
        df=pd.read_csv('C:\Users\ukiws001\Desktop\East Riding\Base csvs\SLA_Request_Oct2021\CSV'+j+i+'SLA_ODMatrix.csv',names=list(range(0,2771)))
        df.drop(0,axis=1, inplace = True)
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
        df.to_csv('C:/Users/ukiws001/Desktop/East Riding/Base csvs/'+j+i+'.csv')
        
        '_B1242S_','A1033_','_A63_HULL_','_A15_','_B1228_S_','_A161_','_M62_'