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

df1 = df1.loc[ df1['items_id'] != 4798 ]
df1 = df1.loc[ df1['items_id'] != 4762 ]
df1 = df1.loc[ df1['items_id'] != 4759 ]
df1 = df1.loc[ df1['items_id'] != 4770 ]
df1 = df1.loc[ df1['items_id'] != 4738 ]
df1 = df1.loc[ df1['items_id'] != 4785 ]
df1 = df1.loc[ df1['items_id'] != 4800 ]
df1 = df1.loc[ df1['items_id'] != 5141 ]
df1 = df1.loc[ df1['items_id'] != 4826 ]

df1.loc[ df1['items_id'] == 2253, 'items_id' ] = 2252
df1.loc[ df1['items_id'] == 3275, 'items_id' ] = 3273

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


# remove duplicates, hand-curated by Charla,
# this code is copied from build_product_db
xlist = []
xl = [3274, 3276, 4749, 4814, 4825]
xlist.append(xl)
xl = [3273, 4752, 4757, 4813, 4824]
xlist.append(xl)
xl = [2252, 2253]
xlist.append(xl)
xl = [2208, 3894, 5445]
xlist.append(xl)
xl = [2210, 4274, 4743, 4766, 4771, 4780, 4789, 4797, 4822]
xlist.append(xl)
xl = [2236, 2304]
xlist.append(xl)
xl = [2237, 2303, 4729, 4761, 4764, 4793, 4811]
xlist.append(xl)
xl = [2238, 4727, 4769, 4773, 4778, 4784]
xlist.append(xl)
xl = [2243, 4731, 4747, 4755]
xlist.append(xl)
xl = [2244, 4730, 4744, 4746, 4754, 4794, 4804, 4821, 4823]
xlist.append(xl)
xl = [2245, 3410]
xlist.append(xl)
xl = [2307, 4781]
xlist.append(xl)
xl = [2716, 4726, 4768, 4777, 4783]
xlist.append(xl)
xl = [3020, 4732, 4748, 4752, 4756]
xlist.append(xl)
xl = [3036, 4788, 4842]
xlist.append(xl)
xl = [3037, 4841]
xlist.append(xl)
xl = [3038, 4786, 4840]
xlist.append(xl)
xl = [3265, 3287, 4725, 4767, 4772, 4776, 4790, 4825, 4837]
xlist.append(xl)
xl = [3285, 4838]
xlist.append(xl)
xl = [3288, 3608, 4728, 4774, 4779, 4791, 4799, 4836]
xlist.append(xl)
xl = [3370, 4792, 4829]
xlist.append(xl)
xl = [3389, 4801, 4830]
xlist.append(xl)
xl = [4734, 4736, 4739, 4740]
xlist.append(xl)
xl = [4735, 4742, 4796, 4816]
xlist.append(xl)
xl = [4775, 4827, 4834]
xlist.append(xl)
xl = [3893, 5142]
xlist.append(xl)
xl = [5446, 5469]
xlist.append(xl)
xl = [1822, 4305, 4312, 4317, 4327]
xlist.append(xl)
xl = [1828, 4331]
xlist.append(xl)
xl = [1829, 4322]
xlist.append(xl)
xl = [1832, 4326]
xlist.append(xl)
xl = [1841, 4334]
xlist.append(xl)
xl = [1847, 4303, 4310, 4316, 4323]
xlist.append(xl)
xl = [1848, 4304, 4311]
xlist.append(xl)
xl = [1849, 4302, 4315, 4336]
xlist.append(xl)
xl = [1850, 4320]
xlist.append(xl)
xl = [3167, 4325]
xlist.append(xl)
xl = [3168, 4335]
xlist.append(xl)
xl = [3170, 4333]
xlist.append(xl)
xl = [3171, 4306, 4313, 4318, 4328]
xlist.append(xl)
xl = [3595, 4329]
xlist.append(xl)
xl = [4307, 4319]
xlist.append(xl)
xl = [1823, 4324]
xlist.append(xl)
xl = [1813, 2205]
xlist.append(xl)
xl = [1838, 3407]
xlist.append(xl)
xl = [1848, 4304, 4311, 3274, 3276, 4749, 4814, 4825]
xlist.append(xl)
xl = [1851, 3273, 4752, 4757, 4813, 4824]
xlist.append(xl)
xl = [1852, 2246]
xlist.append(xl)
xl = [1854, 2248]
xlist.append(xl)
xl = [1856, 2250]
xlist.append(xl)
xl = [1855, 2249]
xlist.append(xl)
xl = [1858, 2252, 2253]
xlist.append(xl)
xl = [3069, 3123]
xlist.append(xl)
xl = [3070, 3124]
xlist.append(xl)
xl = [4307, 4319, 4734, 4736, 4739, 4740]
xlist.append(xl)
xl = [4308, 4735, 4742, 4796, 4816]
xlist.append(xl)

for xl in xlist:
    for x in xl:
        df1.loc[ df1['items_id'] == x, 'items_id' ] = xl[0]

# location 2:
# no changes needed

df1.to_csv("../data/location1_cleaned.csv",index=False,header=True)
#df2.to_csv("../data/location2_cleaned.csv",index=False,header=True)
