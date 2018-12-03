#!/usr/bin/env python3
import sys
import json
import collections
from flask import Flask,render_template,jsonify,request,Response,url_for,\
    redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from data_engineering import product_models as pm
import numpy as np
from forms import *
import logic

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'x839z&,a&**'
app.config['STATIC_FOLDER'] = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/eatsencore.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#engine = db.get_engine()
#session = Session(engine)


# homepage form > menu
@app.route("/",methods=['GET','POST'])
def index():

    form = LandingPageForm()
     
    if request.method == 'POST':
        age_group = form.age_group.data
        return redirect(url_for('menu',age_group=age_group))
        
    
    return render_template("index.html",xpage="index")


# menu order cart > checkout
@app.route("/checkout",methods=['GET','POST'])
def checkout():

    form = MenuForm()   

    if request.method == 'GET':
        return redirect(url_for('index'))

    
    if request.method == 'POST':
        selections = json.loads(form.selections.data)
        age_group = form.age_group.data
        
        print(age_group)
        print(selections)

        order = collections.OrderedDict()
        order['entree'] = {}
        order['kids'] = {}
        order['side'] = {}
        order['dessert'] = {}
        order['beverage'] = {}
        order['alcohol'] = {}

        ordercats = []
        for key in order.keys():
        
            if key in selections.keys():
                ordercats.append(key)
                res = db.session.query(pm.Product).filter(pm.Product.id == \
                                              int(selections[key])).first()

                order[key]['id'] = str(selections[key])
                order[key]['img'] = res.img
                order[key]['name'] = res.name
                order[key]['display_desc'] = res.name

        
        recos = logic.recommend(order,age_group)
        recommendations = []
        for rec in recos:
            md = {}
            res = db.session.query(pm.Product).filter(pm.Product.id == \
                                                   rec).first()

            md['id'] = rec
            md['img'] = res.img
            md['name'] = res.name
            md['display_desc'] = res.name
            
            recommendations.append(md)
            
        print(recommendations)
            
    return render_template("checkout.html",xpage="checkout",
                           order=order,ordercats=ordercats,
                           recommendations=recommendations)

# main nav > stats
@app.route("/stats",methods=['GET','POST'])
def stats():

    return render_template("stats.html",xpage="stats")


# main nav > about 
@app.route("/about",methods=['GET','POST'])
def about():

    return render_template("about.html",xpage="about")


# menu / get products
@app.route("/get_products/<loc_id>",methods=['GET'])
def get_products(loc_id):

    
    try:
        lid = int(loc_id)
    except:
        return Response("{}", status=400, mimetype='application/json')
        
    res = db.session.query(pm.Product).filter(pm.Product.location_id == \
                    int(loc_id)).all()

    xlist = []
    for d in res:
        d.__dict__['category'] = d.category.name
        del d.__dict__['_sa_instance_state']
        xlist.append(d.__dict__)

    return jsonify(xlist)

# filter menu by age group
@app.route("/menu/<age_group>",methods=['GET','POST'])
def menu(age_group):

    loc_id = 1

    res = db.session.query(pm.Category).all()

    #Entrees Call
    entree_cat = db.session.query(pm.Category)\
                .filter(pm.Category.name == 'Entree').first()
    
    entrees = db.session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == entree_cat.id).all()


    #Side Dishes Call
    side_cat = db.session.query(pm.Category)\
                .filter(pm.Category.name == 'Side').first()
    
    side = db.session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == side_cat.id).all()


    #Desserts Call
    dessert_cat = db.session.query(pm.Category)\
                .filter(pm.Category.name == 'Dessert').first()
    
    dessert = db.session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == dessert_cat.id).all()


    #Beverages Call
    beverage_cat = db.session.query(pm.Category)\
                .filter(pm.Category.name == 'Beverage').first()
    
    beverage = db.session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == beverage_cat.id).all()


    # #Adult Boozy Beverages Call
    alcoholicBeverage_cat = db.session.query(pm.Category)\
                 .filter(pm.Category.name == 'Alcoholic Beverage').first()
    
    alcoholicBeverage = db.session.query(pm.Product).filter(pm.Product.location_id == \
                                            int(loc_id))\
             .filter(pm.Product.category_id == alcoholicBeverage_cat.id).all()



    #Kids Call
    kids_cat = db.session.query(pm.Category)\
                .filter(pm.Category.name == 'Kids').first()
    
    kids = db.session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == kids_cat.id).all()


    # remove coffee, decaf, and tea from kids choices
    bevs_filtered = []
    for bev in beverage:
        if bev.id not in [3070,3069,1854]:
            bevs_filtered.append(bev)
    

    if request.method == 'GET':
        return render_template('menu_choose_items.html',age_group=age_group,
                               entrees=entrees,
                               side = side,
                               dessert=dessert,
                               beverage=bevs_filtered,
                               alcoholicBeverage=alcoholicBeverage,
                               kids=kids
                               )



# recommendations added to cart
# @app.route("/summary",methods=['GET','POST'])

#     #Recommendations Call
#     recommendation_cat = db.session.query(pm.Category)\
#                 .filter(pm.Category.name == 'Recommendation').first()
    
#     recommendation = db.session.query(pm.Product).filter(pm.Product.location_id == \
#                                            int(loc_id))\
#             .filter(pm.Product.category_id == recommendation_cat.id).all()



        
              
            
if __name__ == "__main__":
    app.run(debug=True)
