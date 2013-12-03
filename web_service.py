'''
Created on 29/06/2013

@author: raul
'''

from flask import Flask
from flask import request
from mongo_connector import MongoConnector
import json
from bson import json_util

app = Flask(__name__)
connector = MongoConnector()

@app.route("/documents")
def documents():
    fecha_ini = request.args.get('date', None)

    results = connector.find(fecha_ini)
    li_results = list(results)
    print li_results
    json_dict = { "items": li_results, "size": len(li_results)}
    json_doc = json.dumps(json_dict, default=json_util.default, sort_keys=True, indent=2)
    print json_doc
    return json_doc

@app.route("/hello")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
