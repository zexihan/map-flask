from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)
api = Api(app)

types = ["restaurants", "shopping", "nightlife", "expense", "host", "noise", "safety", "transit"]

df_map = {}
for type in types:
    df_map[type] = pd.read_csv("data/" + type + ".csv")

class DescriptiveData(Resource):
    def get(self, type, col):
        df = df_map[type]
        res_list = []
        for i in range(df.shape[0]):
            res_list.append(df.iloc[i][col])
        return res_list
        
api.add_resource(DescriptiveData, '/api/<type>/<col>')

if __name__ == '__main__':
    app.run(debug=True)
