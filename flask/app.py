from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
import csv
import re
from datetime import datetime

datapath = os.path.join(os.path.dirname(__file__), '../db')

def ticker_mapping():

    mapping = dict()
    
    with open(datapath + '/EarningsTranscriptList.csv') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            mapping[row['Ticker']] = row['Company Name']

    return mapping

def str_to_list(string):

    if not string:
        return
    
    string = string.replace('{', '').replace('}', '').strip()

    split_string = string.split('\n')
    new_data = list()
    for ss in split_string:
        new_data.append(ss.replace('"', '').strip())

    return new_data

def str_to_dict(string):

    # Define the replacement function
    def replace_comma(match):
        return match.group().replace(',', '<;>')

    if not string:
        return
    
    string = string.replace('{', '').replace('}', '').strip()

    # Replace commas within quotations using the pattern and replacement function
    new_string = re.sub(r'"([^"]*)"', replace_comma, string)

    split_string = new_string.replace('\n', ',').split(',')

    new_data = dict()
    for ss in split_string:
        if not ss.strip():
            continue
        try:
            key, value = ss.split(":")
            new_data[key.replace('"', '').replace('<;>',',').strip()] = value.replace('"', '').replace('<;>',',').strip()

        except Exception as e:
            print("[DEBUG] THE FOLLOW JSON STRINGS CAUSED SOME PROBLEMS: \n%s\n%s" %(string, split_string))
            print(e,">>",ss)

    return new_data
        

app = Flask(__name__)
CORS(app) # allows same host packet routing

@app.route('/api/getCompanyInfo', methods=['GET'])
def get_q1():
    # Read the JSON file
    mapping = ticker_mapping()

    with open(datapath + '/question1.json') as file:
        json_data = json.load(file)

    processed_data = list()
    
    for old_key, old_value in json_data.items():
        new_record = dict()
        new_key = old_key[:-8]
        calendar_date = datetime.strptime(old_key[-8:], "%Y%m%d").date()
        old_value['financials'] = str_to_dict(old_value.get('financials', None))
        old_value['rating'] = re.search(r'\d+', old_value['rating']).group()
        if old_value.get('compfin',False):
            temp_text = old_value['compfin'].replace('{','').replace('}','').replace(',',' | ').strip()
            old_value['compfin'] = re.sub('\s{2,}', ' ', temp_text)
        new_record['id'] = old_key
        new_record['ticker'] = new_key
        new_record['date'] = calendar_date.strftime("%d/%m/%Y")
        new_record['company'] = mapping[new_key]
        new_record.update(old_value)
        processed_data.append(new_record)
        
    # Return the JSON data
    return processed_data

@app.route('/api/getComparePeers', methods=['GET'])
def get_q3():
    # # Read the JSON file
    # with open(datapath + '/question3.json') as file:
    #     data = file.read()
    
    # # Return the JSON data
    # return jsonify(data)

    with open(datapath + '/question3.json') as file:
        json_data = json.load(file)

    processed_dict = dict()

    for old_key, old_value in json_data.items():
        processed_dict['id'] = old_key
        new_value = dict()
        for k, v in old_value.items():
            if '{' in str(v):
                new_value[k] = eval('%s' %v)
            else:
                new_value[k] = eval('"%s"' %v.replace('"', "'").replace('\n', '').strip())
        processed_dict.update(old_value)

    return processed_dict

if __name__ == '__main__':
    app.run(debug=True)