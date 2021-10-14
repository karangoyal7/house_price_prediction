from flask import Flask, render_template, request
import json
import numpy as np
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    with open('columns.json') as f:
        data = json.load(f)

    x = data['data_columns']
    f.close()

    return render_template("app1.html",x=x[3:])

def ValuePredictor(to_predict_list):
    #to_predict = np.array(to_predict_list).reshape(1, 4)

    with open('columns.json') as f:
        data = json.load(f)

    #f = open('columns.json','r')
    #data = json.loads(f.read())

    x=data['data_columns']
    f.close()

    x1=np.zeros(len(x))
    x1[0]=float(to_predict_list[0])
    x1[1]=int(to_predict_list[1])
    x1[2]=int(to_predict_list[2])
    loc_index=np.where(x==to_predict_list[3])[0]
    if loc_index>=0:
        x1[loc_index]=1
    loaded_model = pickle.load(open("bengaluru_home_prices_model.pickle", "rb"))
    return loaded_model.predict([x1])[0]

@app.route('/result', methods=['GET','POST'])

def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        #to_predict_list = list(map(int, to_predict_list))
        predicted_value = ValuePredictor(to_predict_list)
        prediction = '{} lakhs'.format(predicted_value)
        return render_template("app1.html", prediction=prediction)

if __name__=='__main__':
   app.run()