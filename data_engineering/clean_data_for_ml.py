#!/usr/bin/env python3
import sys
import pandas as pd
import sqlalchemy as sql
import numpy as np
import collections

#read data
if1 = "../data/comissionary_orders.csv"
if2 = "../data/harbor_house_orders.csv"

df1 = pd.read_csv(if1)
df2 = pd.read_csv(if2)


# delete/reassign the following items, based on data cleaning
# in build_product_db:

# location 1:
#xdel_list = [5141,4826]
#xreassing_list = [ (3275,3273)]

df1 = df1.loc[ df1['items_id'] != 5141 ]
df1 = df1.loc[ df1['items_id'] != 4826 ]
df1.loc[ df1['items_id'] == 3275, 'items_id' ] = 3273



# location 2:
# no changes needed

df1.to_csv("../data/location1_cleaned.csv",index=False,header=True)
df2.to_csv("../data/location2_cleaned.csv",index=False,header=True)
