#!/usr/bin/env python3
import sys
import pandas as pd
import sqlalchemy as sql
import numpy as np
import collections

import product_models as pm

# get hand-coded product image file
df_img = pd.read_csv('product_image_mapping.csv')
df_prod = pd.read_csv('products_charla20181128.csv')

# get an engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///../db/eatsencore.sqlite')

# initialize db
from sqlalchemy.orm import sessionmaker
sx = sessionmaker()
sx.configure(bind=engine)
session = sx()
pm.Base.metadata.create_all(engine)

# some helper functions
def fix_price_issues(xdf):

    new_df = xdf.copy()
    
    ids = list(xdf['items_id'])
    dups = [item for item, count in \
            collections.Counter(ids).items() if count > 1]
    dups = set(dups)
    dups = list(dups)

    # delete dups from data frame
    new_df.set_index('items_id',inplace=True)
    new_df.drop(dups,inplace=True)
    new_df.reset_index(drop=False,inplace=True)

    for dup in dups:
        rows = xdf.loc[ xdf['items_id'] == dup ].copy()
        rows['item_price'].apply(lambda x: float(x))
        max_price = rows['item_price'].max()
        rows.loc[:,'item_price'] = f"{max_price:.2f}"
        rows = rows.drop_duplicates()

        if len(rows) > 1:
            for index,row in rows.iterrows():
                print(row['items_id'],row['items_name'],"*",
                          row['display_description'])

        new_df = new_df.append(rows)
    
    return new_df

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

        
def assign_image(xdf,df_img):

    xdf['img'] = None

    df_img = df_img.copy()
    df_img.set_index('id',inplace=True)
    
    for index,row in xdf.iterrows():

        xdf.loc[index,'img'] = df_img.loc[row['items_id'],'img']
        
    return xdf

# Now fill the database
def insert_items(xdf,session,loc_id):

    for index,row in xdf.iterrows():

        #print(row['items_id'],row['items_name'])
        
        item = pm.Product()
        item.id = int(row['items_id'])
        item.name = row['items_name']
        item.price = str(row['item_price'])

        if isinstance(row['display_description'],float): 
            if np.isnan(row['display_description']):
                row['display_description'] = ""
        
        item.display_desc = row['display_description']

        item.img = row['img']
        
        item.location_id = loc_id

        cat = session.query(pm.Category).filter(pm.Category.name \
                                == row['item_category_type']).first()
        item.category_id = cat.id
        session.add(item)

    session.commit()


# two locations:
loc1 = "ABC Commissary"

loc = pm.Location()
loc.name = loc1
session.add(loc)


#read data
if1 = "../data/comissionary_orders.csv"

df1 = pd.read_csv(if1)
#df2 = pd.read_csv(if2)

#print(df1.columns)

ll = list(df1['item_category_type'].drop_duplicates())
ll.sort()

for item in ll:
    cat = pm.Category()
    cat.name = item
    session.add(cat)
session.commit()

# work on location 1
loc_id = 1
xdf = df1[ ['items_id','items_name','item_price',
           'display_description','item_category_type'] ]
xdf = xdf.drop_duplicates()

# manual cleaning -- duplicate items with different prices
# remove items id 5141, 4826
xdf = xdf.loc[ xdf['items_id'] != 5141 ]
xdf = xdf.loc[ xdf['items_id'] != 4826 ]
xdf.loc[ xdf['items_id'] == 3275, 'items_id' ] = 3273
xdf.loc[ xdf['items_id'] == 3273, 'items_name' ] =\
                "Smucker's® Uncrustables® Sandwich"
xdf.loc[ xdf['items_id'] == 2245, 'display_description'] =\
                "Chocolate Cupcake"
xdf.loc[ xdf['items_id'] == 4730, 'display_description'] =\
        "served on an Allergy-friendly Bun with Carrots, "\
        "Apple Slices and choice of Beverage"
xdf.loc[ xdf['items_id'] == 4754, 'display_description'] =\
        "served with Carrots, Apple Slices and choice of Beverage"
xdf.loc[ xdf['items_id'] == 4778, 'display_description'] =\
    "served with Coleslaw and choice of Green Beans,"\
    "Apple Slices or French Fries"
xdf.loc[ xdf['items_id'] == 4794, 'display_description'] =\
        "served on an Allergy-friendly Bun with Carrots, "\
        "Apple Slices and choice of Beverage"



# more name fixing
xdf = fix_product_names(xdf,df_prod)


# remove duplicates, hand-curated by Charla
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
        xdf.loc[ xdf['items_id'] == x, 'items_id' ] = xl[0]

xdf = xdf.drop_duplicates()
xdf = xdf.drop_duplicates(subset='items_id',keep='first')

# more cleaning
xdf = fix_price_issues(xdf)

xdf = assign_image(xdf,df_img)

insert_items(xdf,session,1)



sys.exit()

# done with location 1, ready for location 2    
xdf = df2[ ['items_id','items_name','item_price',
           'display_description','item_category_type'] ]
xdf = xdf.drop_duplicates()
xdf.loc[ xdf['items_id'] == 3593, 'items_name'] =\
   "Harbour Salad with Chicken"
xdf.loc[ xdf['items_id'] == 3594, 'items_name'] =\
    "Harbour Salad with Shrimp"
xdf.loc[ xdf['items_id'] == 1851, 'items_name'] =\
    "Smuckers® Uncrustables®"
xdf.loc[ xdf['items_id'] == 4302, 'display_description'] =\
     "served with Dannon® Danimals® Smoothie,"\
     " GoGo squeeZ® Applesauce and choice of Beverage"
xdf.loc[ xdf['items_id'] == 4313, 'display_description'] =\
    "served with French Fries"
xdf = xdf.drop_duplicates()

xdf = fix_price_issues(xdf)

xdf = assign_image(xdf,df_img)

insert_items(xdf,session,2)
