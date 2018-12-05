#!/usr/bin/env python3
import sys
import collections
import json

# load in popularity model
with open('data/most_popular.json', 'r') as f:
    most_popular = json.load(f)

# load kids model
with open('data/kids_recommendations.json','r') as f:
    kids = json.load(f)

# load teens model
with open('data/teens_recommendations.json','r') as f:
    teens = json.load(f)

# load adults model
with open('data/adults_recommendations.json','r') as f:
    adults = json.load(f)

    
def popularity_recommend(order,age_group):

    reco = []
    base_cats = ['side','dessert','beverage']
    if int(age_group) == 0:
        cats = ['kids']
        cats += base_cats
    elif int(age_group) == 1:
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


def kids_recommend(order):

    age_group = 0
    
    reco = []

    cats = ['kids','side','dessert','beverage']

    # loop over categories
    for cat in cats:
        if len(order[cat]) < 1:
            # need a recommendation for this cat
            keys = [x for x in order.keys() if len(order[x]) > 0]
            xlist = []
            for key in keys:
                xid = order[key]['id']
                if kids[xid][cat] == -1:
                    raise Exception("This should never happen. Fix me!")
                if kids[xid][cat] != -2:
                    xlist.append(kids[xid][cat])

            # sort by largest product of support * confidence * lift
            xsorted = sorted(xlist,key = lambda x: \
                        x['support']*x['confidence']*x['lift'],reverse=True)

            # if we didn't get any recos, recommend the most popular
            if len(xsorted) == 0:
                reco.append(most_popular[cat][0])
            else:
                reco.append(xsorted[0]['id'])

    return reco

def teens_recommend(order):

    age_group = 0
    
    reco = []

    cats = ['entree','side','dessert','beverage']

    # loop over categories
    for cat in cats:
        if len(order[cat]) < 1:
            # need a recommendation for this cat
            keys = [x for x in order.keys() if len(order[x]) > 0]
            xlist = []
            for key in keys:
                xid = order[key]['id']
                if teens[xid][cat] == -1:
                    raise Exception("This should never happen. Fix me!")
                if teens[xid][cat] != -2:
                    xlist.append(teens[xid][cat])

            # sort by largest product of support * confidence * lift
            xsorted = sorted(xlist,key = lambda x: \
                        x['support']*x['confidence']*x['lift'],reverse=True)

            # if we didn't get any recos, recommend the most popular
            if len(xsorted) == 0:
                print("most popular for ",cat)
                reco.append(most_popular[cat][0])
            else:
                print("model for ",cat)
                print(xsorted[0])
                reco.append(xsorted[0]['id'])

    return reco

def adults_recommend(order):

    age_group = 0
    
    reco = []

    cats = ['entree','side','dessert','beverage','alcohol']

    # loop over categories
    for cat in cats:
        if len(order[cat]) < 1:
            # need a recommendation for this cat
            keys = [x for x in order.keys() if len(order[x]) > 0]
            xlist = []
            for key in keys:
                xid = order[key]['id']
                if adults[xid][cat] == -1:
                    raise Exception("This should never happen. Fix me!")
                if adults[xid][cat] != -2:
                    xlist.append(adults[xid][cat])

            # sort by largest product of support * confidence * lift
            xsorted = sorted(xlist,key = lambda x: \
                        x['support']*x['confidence']*x['lift'],reverse=True)

            # if we didn't get any recos, recommend the most popular
            if len(xsorted) == 0:
                print("most popular for ",cat)
                reco.append(most_popular[cat][0])
            else:
                print("model for ",cat)
                print(xsorted[0])
                reco.append(xsorted[0]['id'])

    return reco



def recommend(order,age_group):

    if int(age_group) == 0:
        return kids_recommend(order)

    if int(age_group) == 1:
        return teens_recommend(order)

    if int(age_group) == 2:
        return adults_recommend(order)

        
    return popularity_recommend(order,age_group)


