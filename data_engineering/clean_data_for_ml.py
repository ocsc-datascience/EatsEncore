#!/usr/bin/env python3
import sys
import pandas as pd
import sqlalchemy as sql
import numpy as np
import collections

#read data
if1 = "../data/comissionary_orders.csv"
df_prod = pd.read_csv('products_charla20181128.csv')
#if2 = "../data/harbor_house_orders.csv"

df1 = pd.read_csv(if1)
#df2 = pd.read_csv(if2)


# delete/reassign the following items, based on data cleaning
# in build_product_db:

# location 1:
#xdel_list = [5141,4826]
#xreassing_list = [ (3275,3273)]

df1 = df1.loc[ df1['items_id'] != 5141 ]
df1 = df1.loc[ df1['items_id'] != 4826 ]
df1 = df1.loc[ df1['items_id'] != 4798 ]
df1 = df1.loc[ df1['items_id'] != 4762 ]
df1 = df1.loc[ df1['items_id'] != 4759 ]
df1 = df1.loc[ df1['items_id'] != 4770 ]
df1 = df1.loc[ df1['items_id'] != 4738 ]
df1 = df1.loc[ df1['items_id'] != 4785 ]
df1 = df1.loc[ df1['items_id'] != 4800 ]
df1.loc[ df1['items_id'] == 3275, 'items_id' ] = 3273
df1['location_name'] = 1 

def fix_product_names(xdf,df_prod):

    dfp = df_prod.copy().set_index('id')
    
    for index,row in xdf.iterrows():

        yy = dfp.loc[row['items_id'],'name_short']
        zz = dfp.loc[row['items_id'],'category_corrected']

        
        if isinstance(yy,str):
            xdf.loc[index,'items_name'] = yy

        if isinstance(zz,str):
            xdf.loc[index,'item_category_type'] = zz
        
    return xdf

df1 = fix_product_names(df1,df_prod)


# location 2:
# no changes needed

df1.to_csv("../data/location1_cleaned.csv",index=False,header=True)
#df2.to_csv("../data/location2_cleaned.csv",index=False,header=True)
