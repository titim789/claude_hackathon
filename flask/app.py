from flask import Flask, jsonify
from flask_cors import CORS
import os
import json


datapath = os.path.join(os.path.dirname(__file__), '../db')

app = Flask(__name__)
CORS(app) # allows same host packet routing

@app.route('/q1', methods=['GET'])
def get_q1():
    # Read the JSON file
    with open(datapath + '/question1.json') as file:
        data = file.read()
    
    # Return the JSON data
    return jsonify(data)

@app.route('/q2', methods=['GET'])
def get_q2():
    # Read the JSON file
    with open(datapath + '/question2.json') as file:
        data = file.read()
    
    # Return the JSON data
    return jsonify(data)

@app.route('/q3', methods=['GET'])
def get_q3():
    # Read the JSON file
    with open(datapath + '/question3.json') as file:
        data = file.read()
    
    # Return the JSON data
    return jsonify(data)

if __name__ == '__main__':
    app.run()