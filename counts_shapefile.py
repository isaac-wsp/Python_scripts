import geopandas as gp
import pandas as pd

counts_path = input("Enter the file path to the smv:")
links_path = input("Enter the file path to the links shape-file:")
export_path = input("Enter a file path for the counts shapefile to be saved in:")

counts = pd.read_excel(counts_path,sheet_name = 'Link Flows')
links = gp.read_file(links_path)
links['A-B'] = links['A'].astype('string') + '-' + links['B'].astype('string')
links=links[['A', 'B', 'RDCLASS', 'RDNAME', 'SPDLIM', 'SFCURVE', 'MIDLANE', 'A-B', 'geometry']]
df = counts.iloc[12:,1:70]
inner = ['ID', 'CalVal', 'Area','Ref','Site Location','Dir','Date','Data Type','Duplicate','A-B','A-Node','B-Node',
'Factor','AM Peak','Interpeak','PM Peak','Off Peak','Check','Observed','Modelled','GEH','GEH Pass','Flow Pass','Observed','Modelled',
'GEH','GEH Pass','Flow Pass','Observed','Modelled','GEH','Observed','Modelled','GEH','Observed','Modelled','GEH','GEH Pass','Flow Pass',
'Observed','Modelled','GEH','GEH Pass','Flow Pass','Observed','Modelled','GEH','Observed','Modelled','GEH','Observed','Modelled','GEH',
'GEH Pass','Flow Pass','Observed','Modelled','GEH','GEH Pass','Flow Pass','Observed','Modelled','GEH','Observed','Modelled','GEH']
main = 'main,' * 18
right = 'ALL VEH,'*5 + 'car,' * 5 + 'LGV,' * 3 + 'HGV,' * 3
mid = main.split(',')[:18] + right.split(',')[:16] * 3
top = main + 'AM Peak,'*16 + 'IP,'*16+'PM Peak,'*16
outer = top.split(',')[:66]
levels = [outer,mid,inner]
tuples = list(zip(*levels))
index = pd.MultiIndex.from_tuples(tuples)

df.dropna(axis=1,how="all",inplace=True)
df.columns = index
df = df.iloc[2:]
counts = df.where(df['main']['main']['CalVal'] != 'Exclude')

am = counts[['main','AM Peak']]
ip = counts[['main','IP']]
pm = counts[['main','PM Peak']]

am.columns = inner[:34]
ip.columns = inner[:34]
pm.columns = inner[:34]

am_counts = links.merge(am,on='A-B')
ip_counts = links.merge(ip,on='A-B')
pm_counts = links.merge(pm,on='A-B')

am_counts.drop(['Area','Ref','Duplicate','A-Node','B-Node','Factor','AM Peak','Interpeak','PM Peak','Off Peak','Check'],axis=1, inplace=True)
ip_counts.drop(['Area','Ref','Duplicate','A-Node','B-Node','Factor','AM Peak','Interpeak','PM Peak','Off Peak','Check'],axis=1, inplace=True)
pm_counts.drop(['Area','Ref','Duplicate','A-Node','B-Node','Factor','AM Peak','Interpeak','PM Peak','Off Peak','Check'],axis=1, inplace=True)

am_counts.columns = ['A', 'B', 'RDCLASS', 'RDNAME', 'SPDLIMIT', 'SFC', 'MIDLANE', 'A-B',
       'geometry', 'ID', 'CalVal', 'Site Location', 'Dir', 'Date', 'Data Type',
       'Observed', 'Modelled', 'GEH', 'GEH Pass', 'Flow Pass', 'Observed_CAR',
       'Modelled_CAR', 'GEH_CAR', 'GEH Pass_CAR', 'Flow Pass_CAR', 'Observed_LGV', 'Modelled_LGV',
       'GEH_LGV', 'Observed_HGV', 'Modelled_HGV', 'GEH_HGV']
ip_counts.columns = ['A', 'B', 'RDCLASS', 'RDNAME', 'SPDLIMIT', 'SFC', 'MIDLANE', 'A-B',
       'geometry', 'ID', 'CalVal', 'Site Location', 'Dir', 'Date', 'Data Type',
       'Observed', 'Modelled', 'GEH', 'GEH Pass', 'Flow Pass', 'Observed_CAR',
       'Modelled_CAR', 'GEH_CAR', 'GEH Pass_CAR', 'Flow Pass_CAR', 'Observed_LGV', 'Modelled_LGV',
       'GEH_LGV', 'Observed_HGV', 'Modelled_HGV', 'GEH_HGV']
pm_counts.columns = ['A', 'B', 'RDCLASS', 'RDNAME', 'SPDLIMIT', 'SFC', 'MIDLANE', 'A-B',
       'geometry', 'ID', 'CalVal', 'Site Location', 'Dir', 'Date', 'Data Type',
       'Observed', 'Modelled', 'GEH', 'GEH Pass', 'Flow Pass', 'Observed_CAR',
       'Modelled_CAR', 'GEH_CAR', 'GEH Pass_CAR', 'Flow Pass_CAR', 'Observed_LGV', 'Modelled_LGV',
       'GEH_LGV', 'Observed_HGV', 'Modelled_HGV', 'GEH_HGV']

am_counts = am_counts.astype({'Observed':'float', 'Modelled':'float', 'GEH':'float','Observed_CAR':'float',
       'Modelled_CAR':'float', 'GEH_CAR':'float','Observed_LGV':'float', 'Modelled_LGV':'float',
       'GEH_LGV':'float', 'Observed_HGV':'float', 'Modelled_HGV':'float', 'GEH_HGV':'float'})

ip_counts = ip_counts.astype({'Observed':'float', 'Modelled':'float', 'GEH':'float','Observed_CAR':'float',
       'Modelled_CAR':'float', 'GEH_CAR':'float','Observed_LGV':'float', 'Modelled_LGV':'float',
       'GEH_LGV':'float', 'Observed_HGV':'float', 'Modelled_HGV':'float', 'GEH_HGV':'float'})

pm_counts = pm_counts.astype({'Observed':'float', 'Modelled':'float', 'GEH':'float','Observed_CAR':'float',
       'Modelled_CAR':'float', 'GEH_CAR':'float','Observed_LGV':'float', 'Modelled_LGV':'float',
       'GEH_LGV':'float', 'Observed_HGV':'float', 'Modelled_HGV':'float', 'GEH_HGV':'float'})

am_counts.to_file(export_path + r"\am_counts.shp")
ip_counts.to_file(export_path + r"\ip_counts.shp")
pm_counts.to_file(export_path + r"\pm_counts.shp")
