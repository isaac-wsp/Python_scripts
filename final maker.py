import pandas as pd

am_o=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_am2.csv')
am_o.index=am_o['Cluster']
am_o.drop('Cluster',axis=1,inplace=True)
pm_o=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_pm2.csv')
pm_o.index=pm_o['Cluster']
pm_o.drop('Cluster',axis=1,inplace=True)
ip_o=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_ip2.csv')
ip_o.index=ip_o['Cluster']
ip_o.drop('Cluster',axis=1,inplace=True)

am_d=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_destAM2.csv')
am_d.index=am_d['Cluster']
am_d.drop('Cluster',axis=1,inplace=True)
ip_d=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_destIP2.csv')
ip_d.index=ip_d['Cluster']
ip_d.drop('Cluster',axis=1,inplace=True)
pm_d=pd.read_csv('C:/Users/ukiws001/Desktop/East Riding/full_network_destPM2.csv')
pm_d.index=pm_d['Cluster']
pm_d.drop('Cluster',axis=1,inplace=True)

roads = {'A614_Driff_WB':'_70280_72899_', 'A614_Driff_EB':'_72899_70280_', 'A614_Driff2_EB': '_70252_73545_', 'A614_Driff2_WB':'_73545_70252_',
         'B1249_EB':'_70385_74627_', 'B1249_WB':'_74627_70385_', 'A164_WB': '_78002_70260_', 'A164_EB':'_70260_78002_'}

root='C:/Users/ukiws001/Desktop/East Riding/Link analysis/'


for i in roads.keys():
    writer = pd.ExcelWriter(root+i+'V3.xlsx', engine='openpyxl')
    df=pd.read_excel(root+i+'3.xlsx',sheet_name='AMorigin')
    df.drop(0,inplace=True)
    df.index=df['Unnamed: 0']
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.columns=['L1', 'PCT L1', 'L2', 'PCT L2', 'L3', 'PCT L3', 'L4',
    'PCT L4', 'HGV', 'PCT HGV', 'LGV', 'PCT LGV']
    for k in range(6):
        df.iloc[:,2*k+1]=df.iloc[:,2*k]/am_o.iloc[:,k]
    df.to_excel(writer,sheet_name='AM_origins')
    df=pd.read_excel(root+i+'3.xlsx',sheet_name='AMdestination')
    df.drop(0,inplace=True)
    df.index=df['Unnamed: 0']
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.columns=['L1', 'PCT L1', 'L2', 'PCT L2', 'L3', 'PCT L3', 'L4',
    'PCT L4', 'HGV', 'PCT HGV', 'LGV', 'PCT LGV']
    for k in range(6):
        df.iloc[:,2*k+1]=df.iloc[:,2*k]/am_d.iloc[:,k]
    df.to_excel(writer,sheet_name='AM_destinations')
    df=pd.read_excel(root+i+'3.xlsx',sheet_name='IPorigin')
    df.drop(0,inplace=True)
    df.index=df['Unnamed: 0']
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.columns=['L1', 'PCT L1', 'L2', 'PCT L2', 'L3', 'PCT L3', 'L4',
    'PCT L4', 'HGV', 'PCT HGV', 'LGV', 'PCT LGV']
    for k in range(6):
        df.iloc[:,2*k+1]=df.iloc[:,2*k]/ip_o.iloc[:,k]
    df.to_excel(writer,sheet_name='IP_origins')
    df=pd.read_excel(root+i+'3.xlsx',sheet_name='IPdestination')
    df.drop(0,inplace=True)
    df.index=df['Unnamed: 0']
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.columns=['L1', 'PCT L1', 'L2', 'PCT L2', 'L3', 'PCT L3', 'L4',
    'PCT L4', 'HGV', 'PCT HGV', 'LGV', 'PCT LGV']
    for k in range(6):
        df.iloc[:,2*k+1]=df.iloc[:,2*k]/ip_d.iloc[:,k]
    df.to_excel(writer,sheet_name='IP_destinations')
    df=pd.read_excel(root+i+'3.xlsx',sheet_name='PMorigin')
    df.drop(0,inplace=True)
    df.index=df['Unnamed: 0']
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.columns=['L1', 'PCT L1', 'L2', 'PCT L2', 'L3', 'PCT L3', 'L4',
    'PCT L4', 'HGV', 'PCT HGV', 'LGV', 'PCT LGV']
    for k in range(6):
        df.iloc[:,2*k+1]=df.iloc[:,2*k]/pm_o.iloc[:,k]
    df.to_excel(writer,sheet_name='PM_origins')
    df=pd.read_excel(root+i+'3.xlsx',sheet_name='PMdestination')
    df.drop(0,inplace=True)
    df.index=df['Unnamed: 0']
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.columns=['L1', 'PCT L1', 'L2', 'PCT L2', 'L3', 'PCT L3', 'L4',
    'PCT L4', 'HGV', 'PCT HGV', 'LGV', 'PCT LGV']
    for k in range(6):
        df.iloc[:,2*k+1]=df.iloc[:,2*k]/pm_d.iloc[:,k]
    df.to_excel(writer,sheet_name='PM_destinations')
    writer.save()
    writer.close()

    
