#import modules
import pandas as pd
import numpy as np
#import dataframe of NoHAM zones and clusters
clusters = pd.read_csv('C:/Users/ukiws001/Desktop/East Riding QGIS/North_Zones_v2.10/noham_zones_freeze_2.10.dbf.csv')
clusters.index = list(range(1,2771)) 
#Create multilevel index for dataframes
outside = list()
inside = list()

for i in ('L1', 'L2', 'L3', 'L4', 'HGV', 'LGV'):
    for j in range(1,2771):
        outside.append(i)
        inside.append(j)
        
indices = list(zip(outside, inside))
indices = pd.MultiIndex.from_tuples(indices)
#Extract desired data from clusters dataframe
zones = pd.DataFrame(clusters['Cluster'], index=indices)
#Give 'zones' the same dimensions and index as target dataframes
for i in ('L1', 'L2', 'L3', 'L4', 'HGV', 'LGV'):
    for j in range(1,2771):
        zones.loc[(i,j), 'Cluster'] = clusters.loc[j, 'Cluster']
#lists to iterate through
#roads = {'_78371_72682_':'A614_S_EB', '_72682_78371_':'A614_S_WB', '_72682_76965_':'A614_N_EB', '_76965_72682_':'A614_N_WB'}
roads = {'A614_Driff_WB':'_70280_72899_', 'A614_Driff_EB':'_72899_70280_', 'A614_Driff2_EB': '_70252_73545_', 'A614_Driff2_WB':'_73545_70252_',
         'B1249_EB':'_70385_74627_', 'B1249_WB':'_74627_70385_', 'A164_WB': '_78002_70260_', 'A164_EB':'_70260_78002_'}
times = ['AM', 'IP', 'PM']
directions = ['EB','WB']
for road in roads.keys():
        writer = pd.ExcelWriter('C:/Users/ukiws001/Desktop/East Riding/Link analysis/'+road+'3.xlsx', engine='openpyxl')
        for time in times:
#read in csv
            df = pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/Base csvs/'+time+roads[road]+'.csv')
            df.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1, inplace=True)
            df.index = indices
#first make destination tables (y=dest,x=origin) by transposing user classes                
            L1 = df.loc['L1'].transpose()
            L2 = df.loc['L2'].transpose()
            L3 = df.loc['L3'].transpose()
            L4 = df.loc['L4'].transpose()
            LGV = df.loc['LGV'].transpose()
            HGV = df.loc['HGV'].transpose()
#Add 'sum' columns to the new dataframes
            L1['sum'] = L1[1]
            L2['sum'] = L2[1]
            L3['sum'] = L3[1]
            L4['sum'] = L4[1]
            LGV['sum'] = LGV[1]
            HGV['sum'] = HGV[1]
#Fill in 'sum' columns with sums of the other columns       
            for l in range(2770):
                L1.iloc[l,2770]=L1.iloc[l,0:2770].sum()
                L2.iloc[l,2770]=L2.iloc[l,0:2770].sum()
                L3.iloc[l,2770]=L3.iloc[l,0:2770].sum()
                L4.iloc[l,2770]=L4.iloc[l,0:2770].sum()
                LGV.iloc[l,2770]=LGV.iloc[l,0:2770].sum()
                HGV.iloc[l,2770]=HGV.iloc[l,0:2770].sum()
#make sure indices match        
            L1.index=clusters.index
            L2.index=clusters.index
            L3.index=clusters.index
            L4.index=clusters.index
            LGV.index=clusters.index
            HGV.index=clusters.index
#Add cluster column to dataframes, then sum trips to each cluster        
            L1 = pd.concat([L1['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
            L2 = pd.concat([L2['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
            L3 = pd.concat([L3['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
            L4 = pd.concat([L4['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
            LGV = pd.concat([LGV['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
            HGV = pd.concat([HGV['sum'],clusters['Cluster']],axis=1).groupby(by='Cluster').sum()
#Add percentage column of percentage of total trips along link going to each cluster        
            L1['PCT'] = L1['sum']/L1['sum'].sum()
            L2['PCT'] = L2['sum']/L2['sum'].sum()
            L3['PCT'] = L3['sum']/L3['sum'].sum()
            L4['PCT'] = L4['sum']/L4['sum'].sum()
            LGV['PCT'] = LGV['sum']/LGV['sum'].sum()
            HGV['PCT'] = HGV['sum']/HGV['sum'].sum()
            L1.columns = ['Trips', 'PCT']
            L2.columns = ['Trips', 'PCT']
            L3.columns = ['Trips', 'PCT']
            L4.columns = ['Trips', 'PCT']
            LGV.columns = ['Trips', 'PCT']
            HGV.columns = ['Trips', 'PCT']
#Create index for final dataframe                
            outer = list()
            inner = list()
            for k in ('L1', 'L2', 'L3', 'L4', 'HGV', 'LGV'):
                for l in ['Trips', 'PCT']:
                    outer.append(k)
                    inner.append(l)
            indices2 = list(zip(outer, inner))
            indices2 = pd.MultiIndex.from_tuples(indices2)
#Create final data frame and add data to it            
            Final = pd.DataFrame(np.empty([22,12]), index = L1.index, columns = indices2)        
            Final['L1'] = L1
            Final['L2'] = L2
            Final['L3'] = L3
            Final['L4'] = L4
            Final['LGV'] = LGV
            Final['HGV'] = HGV
#Save dataframe to excel file for the road, with sheet names for time and direction
            Final.to_excel(writer, sheet_name=time+'destination')
#Now making origins datafram-df has not been touched and is still original data.  Adding sum column.
            df['sum'] = df['1']
            for k in range(2770*6):
                df.iloc[k,2770] = df.iloc[k, 0:2770].sum()
#Create new dataframe of only sum column, and concat with zones                    
            total = df.iloc[:,2770:]
            df = pd.concat([total,zones],axis=1)
#Split df into 6 user classes and sum each by cluster                  
            L1 = df.loc['L1'].groupby('Cluster').sum()
            L2 = df.loc['L2'].groupby('Cluster').sum()
            L3 = df.loc['L3'].groupby('Cluster').sum()
            L4 = df.loc['L4'].groupby('Cluster').sum()
            LGV = df.loc['LGV'].groupby('Cluster').sum()
            HGV = df.loc['HGV'].groupby('Cluster').sum()
#until line 150 is the same procedure as for destination data                
            L1['PCT'] = L1['sum']/L1['sum'].sum()
            L2['PCT'] = L2['sum']/L2['sum'].sum()
            L3['PCT'] = L3['sum']/L3['sum'].sum()
            L4['PCT'] = L4['sum']/L4['sum'].sum()
            LGV['PCT'] = LGV['sum']/LGV['sum'].sum()
            HGV['PCT'] = HGV['sum']/HGV['sum'].sum()
            L1.columns = ['Trips', 'PCT']
            L2.columns = ['Trips', 'PCT']
            L3.columns = ['Trips', 'PCT']
            L4.columns = ['Trips', 'PCT']
            LGV.columns = ['Trips', 'PCT']
            HGV.columns = ['Trips', 'PCT']
                    
            outer = list()
            inner = list()
            for k in ('L1', 'L2', 'L3', 'L4', 'HGV', 'LGV'):
                for l in ['Trips', 'PCT']:
                    outer.append(k)
                    inner.append(l)

            indices2 = list(zip(outer, inner))
            indices2 = pd.MultiIndex.from_tuples(indices2)
            
            Final = pd.DataFrame(np.empty([22,12]), index = L1.index, columns = indices2)
            
            Final['L1'] = L1
            Final['L2'] = L2
            Final['L3'] = L3
            Final['L4'] = L4
            Final['LGV'] = LGV
            Final['HGV'] = HGV
            Final.to_excel(writer, sheet_name=time+'origin')
#Save and close excel sheet at the end of each road iteration
        writer.save()
        writer.close()
