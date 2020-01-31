import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import datetime
from datetime import date




app = Flask(__name__)
model = pickle.load(open('model_predictor.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    genrelist=['Genre_alternativerock',
       'Genre_ambient', 'Genre_classical', 'Genre_country', 'Genre_danceedm',
       'Genre_deephouse', 'Genre_disco', 'Genre_drumbass', 'Genre_dubstep',
       'Genre_electronic', 'Genre_folksingersongwriter', 'Genre_hiphoprap',
       'Genre_indie', 'Genre_latin', 'Genre_metal', 'Genre_pop',
       'Genre_rbsoul', 'Genre_reggaeton', 'Genre_rock', 'Genre_trap']
    features = [(x) for x in request.form.values()]
    #NOW = datetime.date.today()
    NOW=datetime.datetime.strptime('20190227','%Y%m%d').date()
    features[4]=features[4].replace('-','')
    datereleased=datetime.datetime.strptime(features[4],'%Y%m%d').date()
    diff_days = (NOW - datereleased).days
    predictor_feature=[]
    predictor_feature.append(features[0])  #comment
    predictor_feature.append(features[1])  #like
    predictor_feature.append(features[2])  #popularity
    predictor_feature.append(int(features[1])/diff_days)  #likeperdate
    predictor_feature.append(int(features[2])/diff_days)  #popularityperdate
    predictor_feature.append(features[3])  #followers
    for genre in genrelist:
        if(features[5]==genre):
             predictor_feature.append(1)
        else:
            predictor_feature.append(0)

    #output=predictor_feature
    final_features = [np.array(predictor_feature)]
    prediction = model.predict(final_features)

    output = round(prediction[0])

    return render_template('index.html', prediction_text='Song view will be {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)