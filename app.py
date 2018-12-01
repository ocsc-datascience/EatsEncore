#!/usr/bin/env python3
import sys
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

engine = db.get_engine()
session = Session(engine)


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

    # form = shoppingBasket()
    
    # if request.method == 'POST':
    #     orderCart = form.orderCart.data
    #     return redirect(url_for('checkout',orderCart=orderCart))
        
    
    return render_template("checkout.html",xpage="checkout")

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
        
    res = session.query(pm.Product).filter(pm.Product.location_id == \
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

    res = session.query(pm.Category).all()
    for cat in res:
        print(cat.name) 

    

    #Entrées Call
    entree_cat = session.query(pm.Category)\
                .filter(pm.Category.name == 'Entree').first()
    
    entrees = session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == entree_cat.id).all()


    #Side Dishes Call
    side_cat = session.query(pm.Category)\
                .filter(pm.Category.name == 'Side').first()
    
    side = session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == side_cat.id).all()


    #Desserts Call
    dessert_cat = session.query(pm.Category)\
                .filter(pm.Category.name == 'Dessert').first()
    
    dessert = session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == dessert_cat.id).all()


    #Beverages Call
    beverage_cat = session.query(pm.Category)\
                .filter(pm.Category.name == 'Beverage').first()
    
    beverage = session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == beverage_cat.id).all()


    # #Adult Boozy Beverages Call
    # alcoholicBeverage_cat = session.query(pm.Category)\
    #             .filter(pm.Category.name == 'alcoholicBeverage').first()
    
    # alcoholic_Beverage = session.query(pm.Product).filter(pm.Product.location_id == \
    #                                        int(loc_id))\
    #         .filter(pm.Product.category_id == alcoholicBeverage_cat.id).all()



    #Beverages Call
    kids_cat = session.query(pm.Category)\
                .filter(pm.Category.name == 'Kids').first()
    
    kids = session.query(pm.Product).filter(pm.Product.location_id == \
                                           int(loc_id))\
            .filter(pm.Product.category_id == kids_cat.id).all()



    #Request after all category calls have been made—THIS STAYS AT BOTTOM
    if request.method == 'GET':
        return render_template('menu_choose_items.html',age_group=age_group,
                               entrees=entrees,
                               side = side,
                               dessert=dessert,
                               beverage=beverage,
                               #alcoholicBeverage=alcoholicBeverage,
                               kids=kids
                               )



        
              
            
if __name__ == "__main__":
    app.run(debug=True)
