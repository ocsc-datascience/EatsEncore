#!/usr/bin/env python3
import sys
import collections
import json

# load in popularity model
with open('data/most_popular.json', 'r') as f:
    most_popular = json.load(f)


def recommend(order,age_group):

    reco = []
    base_cats = ['side','dessert','beverage']
    if age_group == 0:
        cats = ['kids']
        cats += base_cats
    elif age_group == 1:
          cats = ['entree']
          cats += base_cats
    else:
        cats = ['entree']
        cats += base_cats
        cats += ['alcohol']
    
    keys = list(order.keys())

    for cat in cats:
        if len(order[cat]) < 1:
            reco.append(most_popular[cat][0])

    return reco

