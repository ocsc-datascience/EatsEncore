#!/usr/bin/env python3
import sys
import pandas as pd
import sqlalchemy as sql
import numpy as np
import collections

import product_models as pm

# get hand-coded product image file
df_img = pd.read_csv('product_image_mapping.csv')

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

# remove duplicates
xlist = []
xl = [3274, 3276, 4749, 4814, 4825]
xlist.append(xl)
#xl = [3273, 4752, 4757, 4813, 4824]
#xlist.append(xl)
#xl = [2252, 2253]
#xlist.append(xl)
#xl = [2208, 3894, 5445]
#xlist.append(xl)
#xl = [2210, 4274, 4743, 4766, 4771, 4780, 4789, 4797, 4822]
#xlist.append(xl)
#xl = [2236, 2304]
#xlist.append(xl)

for xl in xlist:
    for x in xl:
        xdf.loc[ xdf['items_id'] == x, 'items_id' ] = xl[0]



    

xdf = xdf.drop_duplicates()

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
