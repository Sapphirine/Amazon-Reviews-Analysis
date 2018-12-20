from flask import Flask, render_template, request, flash, redirect, url_for,session
from wtforms import Form, StringField, validators, TextAreaField
import os
import sys
import numpy as np
import pandas as pd
import json
import sqlite3
from PIL import Image
import requests
from io import BytesIO

pos = pd.read_csv('/Users/srivatsanramesh/Desktop/SQL/positive_features.csv')
neg = pd.read_csv('/Users/srivatsanramesh/Desktop/SQL/negative_features.csv')
app = Flask(__name__,static_folder='/Users/srivatsanramesh/Desktop/Reviews/static',static_url_path='/static')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return redirect('/search')

@app.route('/login',methods=['POST'])
def login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        session['logged_in'] = False
    return home()

def ratings(asin):
    with sqlite3.connect('/Users/srivatsanramesh/Desktop/SQL/final_ratings.db') as conn2:
        cur2 = conn2.cursor()
        cur2.execute('Select overall_final_so,Rating from final_ratings where ID=?',(asin,))
        row2 = cur2.fetchall()
        SO = row2[0][0]
        Avg_rating = row2[0][1]
        cur2.close()
        return SO,Avg_rating

def image(item):
    with sqlite3.connect('/Users/srivatsanramesh/Desktop/SQL/metadata.db') as conn:
        cur = conn.cursor()
        cur.execute('Select asin,imUrl,price from metadata where title=?',(str(item),))
        rows = cur.fetchall()
        asin = rows[0][0]
        img = rows[0][1]
        price = rows[0][2]
        #categories = rows[0][3]
        cur.close()
        return asin,img,price
def positive(asin):
    return pos[pos['asin'] == asin]['pos'].values,pos[pos['asin'] == asin]['count'].values
def negative(asin):
    return neg[neg['asin'] == asin]['neg'].values,neg[neg['asin'] == asin]['count'].values


@app.route('/dashboard/<item>')
def dashboard(item):
    asin,img,price = image(item)
    SO,Avg_rating = ratings(asin)
    return render_template("title.html",content=item,img=img,asin=asin,price=price,SO=round(float(SO),2),Avg_rating=round(float(Avg_rating),2))

@app.route('/pros/<item>')
def pros(item):
    with sqlite3.connect('/Users/srivatsanramesh/Desktop/SQL/metadata.db') as conn:
        cur = conn.cursor()
        cur.execute('Select asin from metadata where title=?',(item,))
        rows = cur.fetchall()
        asin = rows[0][0]
        cur.close()
    pos,percentage = positive(asin)
    return render_template("pros.html",content=item,positive=pos,percentage=percentage)

@app.route('/cons/<item>')
def cons(item):
    with sqlite3.connect('/Users/srivatsanramesh/Desktop/SQL/metadata.db') as conn:
        cur = conn.cursor()
        cur.execute('Select asin from metadata where title=?',(item,))
        rows = cur.fetchall()
        asin = rows[0][0]
        cur.close()
    neg,percentage = negative(asin)
    return render_template("cons.html",content=item,negative=neg,percentage=percentage)

@app.route('/purchase/<item>')
def purchase(item):
    with sqlite3.connect('/Users/srivatsanramesh/Desktop/SQL/purchase.db') as conn:
        cur = conn.cursor()
        cur.execute('Select link from purchase where title=?',(item,))
        rows = cur.fetchall()
        link = rows[0][0]
        cur.close()
    return render_template("purchase.html",link=link,content=item)


@app.route("/logout",methods=['GET'])
def logout():
    if request.method == 'GET':

        session['logged_in'] = False
        return render_template("login.html")

@app.route('/search',methods=["GET","POST"])
def search():
    if request.method == "POST":
        search = request.form['search']
        return redirect(url_for('dashboard',item=search))
    return render_template("search.html")

if __name__ == '__main__':
    app.secret_key="srivatsanramesh"
    app.run(debug = True)
