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
            res_json = {}
            res_json["nbhId"] = df.iloc[i]["neighbourhood"]
            res_json[col] = float(df.iloc[i][col])
            res_list.append(res_json)
        return res_list

nlp_df = pd.read_csv("data/nlp.csv")
nlp_df = nlp_df.replace({pd.np.nan: None})

class NLPData(Resource):
    def get(self):
        res_list = []
        for i in range(nlp_df.shape[0]):
            res_json = {}
            res_json["nbhId"] = nlp_df.iloc[i]["neighbourhood"]
            res_json["clusterSum"] = nlp_df.iloc[i]["cluster_sum"]
            columns = ["noise", "safety", "entertainment", \
                       "restaurant", "host", "expense", "shopping", "nightlife", "transit"]
            for col in columns:
                topic_list = []
                for j in range(1, 6):
                    topic_list.append(nlp_df.iloc[i][col + "_" + str(j)])
                res_json[col] = topic_list
            res_list.append(res_json)
        return res_list
    
class NLPDataNbh(Resource):
    def get(self, nbh_idx):
        nbh_idx = int(nbh_idx)
        res_json = {}
        res_json["nbhId"] = nlp_df.iloc[nbh_idx]["neighbourhood"]
        res_json["clusterSum"] = nlp_df.iloc[nbh_idx]["cluster_sum"]
        columns = ["noise", "safety", "entertainment", \
                   "restaurant", "host", "expense", "shopping", "nightlife", "transit"]        
        for col in columns:
            topic_list = []
            for j in range(1, 6):
                topic_list.append(nlp_df.iloc[nbh_idx][col + "_" + str(j)])
            res_json[col] = topic_list
        return res_json

scores_df = pd.read_csv("data/scores.csv")

class ScoresData(Resource):
    def get(self):
        res_list = []
        for i in range(scores_df.shape[0]):
            res_json = {}
            res_json["nbhId"] = scores_df.iloc[i]["neighbourhood"]
            columns = ["noise", "safety", "shopping", \
                       "restaurant", "nightlife", "expense", "transit"]
            for col in columns:
                res_json[col] = float(scores_df.iloc[i][col])
            res_list.append(res_json)
        return res_list

class ScoresDataNbh(Resource):
    def get(self, nbh_idx):
        nbh_idx = int(nbh_idx)
        res_json = {}
        res_json["nbhId"] = scores_df.iloc[nbh_idx]["neighbourhood"]
        columns = ["noise", "safety", "shopping", \
                   "restaurant", "nightlife", "expense", "transit"]
        for col in columns:
            res_json[col] = float(scores_df.iloc[nbh_idx][col])
        return res_json

api.add_resource(DescriptiveData, '/api/<type>/<col>')
api.add_resource(NLPData, '/api/nlp')
api.add_resource(NLPDataNbh, '/api/nlp/<nbh_idx>')
api.add_resource(ScoresData, '/api/scores')
api.add_resource(ScoresDataNbh, '/api/scores/<nbh_idx>')

if __name__ == '__main__':
    app.run(debug=True)
