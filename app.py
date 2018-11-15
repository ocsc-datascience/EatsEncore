#!/usr/bin/env python3
import sys
from flask import Flask, render_template,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np

app = Flask(__name__)
CORS(app)

#app.config['STATIC_FOLDER'] = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/eatsencore.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Base = automap_base(metadata=db.metadata)
engine = db.get_engine()
Base.prepare(engine, reflect=True)
#Superfund = Base.classes.superfund
#LifeExpectancy = Base.classes.life_expectancy
# load the state stats table
#StateCombinedStats = Base.classes.state_combined_stat


@app.route("/")
def index():

    return render_template("index.html",xpage="index")


if __name__ == "__main__":
    app.run(debug=True)
