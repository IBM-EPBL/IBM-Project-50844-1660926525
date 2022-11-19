import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

import inputScript
 

app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl','rb'))

@app.route('/web detection.html')
def Home():
    return render_template("web detection.html")

@app.route('/web detection',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    url = request.form['URL']
    
    Checkprediction = inputScript.main(url)
    prediction = model.predict(Checkprediction)
    print(prediction)
    output=prediction[0] 
    if (output==1):
        pred="Your are safe!! This is a Legitimate Website."
        
    else:
        pred="Your are on the wrong site. Be cautious!"
    return render_template('final.html',prediction_text='{}'.formate(pred),url=url)

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''   
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.value()))])
    
    output = prediction[0]
    return jsonify(output)


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)