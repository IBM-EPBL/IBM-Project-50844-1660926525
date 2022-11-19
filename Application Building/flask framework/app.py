#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

file = open("demo/model.pkl","rb")
phishing = pickle.load(file)
file.close()


app = Flask(__name__)


@app.route('/')
@app.route('/web detection.html')
def Home():
       return render_template("web detection.html")    
    
@app.route('/')
@app.route('/About.html')
def About():
       return render_template("About.html")


@app.route('/Getstarted.html')
def Getstarted():
       return render_template("Getstarted.html")


@app.route('/Contact.html')
def Contact():
       return render_template("Contact.html")


@app.route("/predict", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred =phishing.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = phishing.predict_proba(x)[0,0]
        y_pro_non_phishing = phishing.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        # pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('predict.html',xx =["It is {0:.2f} % Safe to go ".format(y_pro_non_phishing*100), "It is {0:.2f} % Unsafe to go ".format(y_pro_phishing*100)],url=url)
        # else:
        #     return render_template("predict.html", xx ="Your are on the wrong site. Be cautious!")


if __name__ == "__main__":
    app.run(debug=True,port=5000, host='0.0.0.0')