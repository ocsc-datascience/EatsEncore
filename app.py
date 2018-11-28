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


@app.route("/",methods=['GET','POST'])
def index():

    form = LandingPageForm()
    
    if request.method == 'POST':
        age_group = form.age_group.data
        return redirect(url_for('menu',age_group=age_group))
        
    
    return render_template("index.html",xpage="index")

@app.route("/get_products/<loc_id>",methods=['GET'])
def get_products(loc_id):

    engine = db.get_engine()
    session = Session(engine)
    
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

@app.route("/menu/<age_group>",methods=['GET','POST'])
def menu(age_group):

    if request.method == 'GET':
        return render_template('menu_choose_items.html',age_group=age_group)

        
            
            
if __name__ == "__main__":
    app.run(debug=True)
