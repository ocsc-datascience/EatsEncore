#!/usr/bin/env python3
import sys
import pandas as pd
import sqlalchemy as sql
import numpy as np
import collections

import product_models as pm

# get an engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///../db/eatsencore.sqlite')

# initialize db
from sqlalchemy.orm import sessionmaker
sx = sessionmaker()
sx.configure(bind=engine)
session = sx()


dlist = []
prods = session.query(pm.Product).all()


for prod in prods:

    xd = collections.OrderedDict()
    xd['id'] = prod.id
    xd['name'] = prod.name
    xd['display_desc'] = prod.display_desc
    xd['category'] = prod.category.name
    xd['img'] = prod.img
    #xd['location'] = prod.location.name
    
    dlist.append(xd)


df = pd.DataFrame(dlist)
df.to_csv('products_clean.csv',index=False,header=True)

