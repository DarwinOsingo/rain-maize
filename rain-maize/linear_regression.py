#location_type,terrain,climate,soil_type,construction_season,road_length_km,road_width_m,num_workers,dist_supplier_km,num_bridges,num_culverts,total_cost_KES_M
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

df = pd.read_csv('kenya_roads.csv')




df = pd.get_dummies(df,columns=["location_type","climate","construction_season","terrain","soil_type"],drop_first=True    )
df = df.drop(columns=['project_id'])
