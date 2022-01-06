import pandas as pd
import geopandas as gp

#testing branching

study_zones = [435,438,439,440,446,447,448,450,453,454,461,462,464,465,468,
               473,477,478,484,487,488,491,492,497,498,502,503,504,506,509,
               510,512,517,518,520,522,523,524,525,529,530,534,536,537,539,
               541,542,543,544,546,547,554,555,557,558,559,560,561,568,637,638,
               639,640,641,651]
			   
zone_rename={435:'Radcliffe',438:'Unsworth',439:'Bury',440:'Hapton',446:'NW_Manchester',
			   447:'Rawtenstall',448:'Bacup',450:'SW_Burnley',453:'Blackfriars Manchester',
			   454:'South_Burnley', 461:'North_Burnley',462:'Heywood',464:'NE_Manchester',465:'East_Burnley',
               468:'Blackley', 473:'NW_Rochdale',477:'Middleton',478:'Clayton_Vale',484:'Newton_Heath',
			   487:'Moston',488:'Openshaw',491:'Sudden',492:'Mereclough',497:'Failsworth',498:'Rochdale',
			   502:'Droylsden',503:'Firwood_Park',504:'Butler_Green',506:'Royton',509:'Balderstone',
               510:'Littlemoss',512:'Woodhouses',517:'Hollinwood',518:'North_Rochdale',520:'Freehold',
			   522:'NW_Oldham',523:'Todmorden',524:'Luzley_Brook',525:'Oldham',529:'Taunton',530:'High_Crompton',
			   534:'Ashton-under-Lyne',536:'SE_Oldham',537:'North_Oldham',539:'Derker',541:'Park_Bridge',542:'Tameside',
			   543:'Littleborough',544:'Shaw',546:'East_Rochdale',547:'Piethorne_Valley',554:'Stalybridge', 555:'Buckton_Vale',557:'Springhead',
			   558:'Diggle',559:'Moorside',560:'Waterhead',561:'Mossley',568:'Greenfield',637:'N.O.M.A',638:'Monsall',
               639:'North Manchester',640:'Smedley',641:'Cheetwood',651:'Prestwich'}
string_zones = ['unique_id',  'geometry']

for zone in study_zones:
    string = zone_rename[zone]
    string_zones.append(string)

drop_zones = [1,2,3,4,5,44,53,64,66,67,68,246,247,248,249,259,293,294,295,296,
297,298,299,300,301,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,319,320,321,322,
323,324,325,326,327,328,329,330,331,332,333,334,335,302,336,337,338,339,340,18,23,25,26,47,48,55,
78,79,80,81,82,83,84,85,187,188,189,236,342,343,344,345,346,347,348,349,350,351,352,353,354,355,
356,357,14,15,16,17,19,20,21,22,24,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,50,51,52,56,
57,58,59,60,61,62,63,70,73,74,77,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,
106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,
133,134,135,136,137,147,148,149,150,151,152,153,154,155,157,158,159,161,162,163,164,165,166,167,175,177,178,
180,181,182,183,184,185,186,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,
210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,250,
251,252,253,254,255,256,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,
281,282,283,284,285,286,287,288,289,290,291,292]

zones = gp.read_file(r"C:\Projects\TfN Rail\04 - Multi Modal Data\norms_zoning\noham_zones_freeze_2.10.shp")

norms = gp.read_file(r"C:\Projects\TfN Rail\04 - Multi Modal Data\norms_zoning\zone_system\Norms_Zones-2.11\norms_zoning_freeze_2.11.shp")

new_zones = gp.read_file(r"C:\Projects\TfN Rail\zoning_system.shp")

Folders = {"Bus":r"C:\Projects\TfN Rail\04 - Multi Modal Data\Bus - People Units - Hourly Average\synthetic_od",
            "Highway":r"C:\Projects\TfN Rail\04 - Multi Modal Data\Highway - PCU - Hourly Average\od"}

file_paths =   {"Business_1":"_business_yr2018_m5_tp1.csv",
                "Business_2":"_business_yr2018_m5_tp2.csv",
                "Business_3":"_business_yr2018_m5_tp3.csv",
                "Business_4":"_business_yr2018_m5_tp4.csv",
                "Commute_1":"_commute_yr2018_m5_tp1.csv",
                "Commute_2":"_commute_yr2018_m5_tp2.csv",
                "Commute_3":"_commute_yr2018_m5_tp3.csv",
                "Commute_4":"_commute_yr2018_m5_tp4.csv",
                "Other_1":"_other_yr2018_m5_tp1.csv",
                "Other_2":"_other_yr2018_m5_tp2.csv",
                "Other_3":"_other_yr2018_m5_tp3.csv",
                "Other_4":"_other_yr2018_m5_tp4.csv"}

purposes = ['Business', 'Commute', 'Other']

times = ['1','2','3','4']


    
for time in times:
    folder = r"C:\Projects\TfN Rail\04 - Multi Modal Data\Highway - PCU - Hourly Average\od"
    OD1 = pd.read_csv(folder + file_paths["Business_" + time])
    OD2 = pd.read_csv(folder + file_paths["Commute_" + time])
    OD3 = pd.read_csv(folder + file_paths["Other_" + time])
    OD = OD1 + OD2 + OD3
    OD.rename({'Unnamed: 0':'id'},axis=1,inplace=True)
    trans =OD.transpose()
    trans.drop('id',axis=0,inplace=True)
    trans.index = OD.index
    trans.columns = range(1,1301)
    trans['id'] = range(1,1301)
    new = norms.merge(trans,on = 'id')
    Large = new.groupby('zone').sum()
    Large.drop(['id'],axis = 1,inplace = True)
    local_auth = Large.transpose()
    local_auth['id'] = range(1,1301)
    local_auth = local_auth.merge(norms,on='id')
    local_auth.index = range(1,1301)
    final = local_auth.groupby('zone').sum()
    destinations = final.loc[:,study_zones]
    origins = final.transpose()
    origins = origins.loc[:,study_zones]
    origins.drop('id',axis=0,inplace=True)
    origins['unique_id'] = origins.index
    destinations['unique_id'] = origins.index
    origins = new_zones.merge(origins,on='unique_id')
    destinations = new_zones.merge(destinations,on='unique_id')
    origins.columns = string_zones
    destinations.columns = string_zones
    package =folder +  "{}.gpkg"
    origins.to_file(package.format("Highway"), layer = 'origins_' + time, driver = "GPKG" )
    destinations.to_file(package.format("Highway"), layer = 'destinations_' + time, driver = "GPKG" )