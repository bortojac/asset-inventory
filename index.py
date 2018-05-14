from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
import createReports
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/', methods = ['GET', 'POST'])
def data():
    store = request.args['store']
    invDict = { 'bonds': int(request.args['bond']), 'stocks': int(request.args['stock']), 'options': int(request.args['option']) }
    if store == 'Company2':
        return jsonify(createReports.calculateCompany2(company2StartInv=invDict)['company2DF'].to_json(orient="records"))
    elif store == 'Company1':
        return jsonify(createReports.calculateCompany1(company1StartInvDict=invDict)['company1DF'].to_json(orient="records"))
    
if __name__ == '__main__':
    app.run()
