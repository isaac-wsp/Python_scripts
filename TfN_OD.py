import pandas as pd
import geopandas as gp

zones = gp.read_file(r"C:\Projects\TfN Rail\04 - Multi Modal Data\norms_zoning\noham_zones_freeze_2.10.shp")
zones.drop(['zone_name', 'zone_cat', 'internal', 'anlytl_sec', 'inner_ldn',
       'outer_ldn', 'met_area', 'urban_big', 'urban_lge', 'urban_med',
       'urban_sml', 'rural', 'area_noh', 'origin_pop', 'ca_sector'],axis=1,inplace=True)
zones.head()

Folders = (r"C:\Projects\TfN Rail\04 - Multi Modal Data\Bus - People Units - Hourly Average\synthetic",
            r"C:\Projects\TfN Rail\04 - Multi Modal Data\Bus - People Units - TP Totals\synthetic")

file_paths =   {"Business_1":"_od_business_yr2018_m5_tp1.csv",
                "Business_2":"_od_business_yr2018_m5_tp2.csv",
                "Business_3":"_od_business_yr2018_m5_tp3.csv",
                "Business_4":"_od_business_yr2018_m5_tp4.csv",
                "Commute_1":"_od_commute_yr2018_m5_tp1.csv",
                "Commute_2":"_od_commute_yr2018_m5_tp2.csv",
                "Commute_3":"_od_commute_yr2018_m5_tp3.csv",
                "Commute_4":"_od_commute_yr2018_m5_tp4.csv",
                "Other_1":"_od_other_yr2018_m5_tp1.csv",
                "Other_2":"_od_other_yr2018_m5_tp2.csv",
                "Other_3":"_od_other_yr2018_m5_tp3.csv",
                "Other_4":"_od_other_yr2018_m5_tp4.csv"}
for folder in Folders:
    for time in file_paths.keys():
        OD = pd.read_csv(folder + file_paths[time])
        OD.rename({'Unnamed: 0':'id'},axis=1,inplace=True)
        trans =OD.transpose()
        trans.drop('id',axis=0,inplace=True)
        trans.index = OD.index
        trans.columns = range(1,2771)
        trans['id'] = range(1,2771)
        new = zones.merge(trans,on = 'id')
        Large = new.groupby('Local Auth').sum()
        Small = new.groupby('NORMS').sum()
        Large.drop(['id','NORMS'],axis = 1,inplace = True)
        Small.drop(['id','Local Auth'],axis = 1,inplace = True)
        local_auth = Large.transpose()
        NORMS = Small.transpose()
        local_auth['id'] = range(1,2771)
        NORMS['id'] = range(1,2771)
        local_auth = local_auth.merge(zones,on='id')
        NORMS = NORMS.merge(zones,on='id')
        local_auth.index = range(1,2771)
        NORMS.index = range(1,2771)
        local = local_auth.groupby('Local Auth').sum()
        NORM = NORMS.groupby('NORMS').sum()
        
        local.to_csv(folder+time+"local.csv")
        NORM.to_csv(folder+time+"NORMS.csv")





