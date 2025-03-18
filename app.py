from parse_request import ParseEssentials
from flask import Flask, request, jsonify
from flask_cors import CORS
from flight_scrapper import *
from flight_elasticSearch import *
import os
import json
flight_app = Flask(__name__)
CORS(flight_app)  # Allow cross-origin requests from any domain


@flight_app.route('/extract-flight-info', methods=['POST'])
def extract_flight_info():
    data = request.json
    user_input = data.get("text", "")

    flight_info  = ParseEssentials()
    flight_info.get_flight_info(user_input)

    res = Scrape(flight_info.src, flight_info.dst, flight_info.date)
    print(res)
    res_json = res.to_json()
    create_index()
    insert_data(res_json)
    res = query()
    print(res)
    return res #jsonify(res)



if __name__ == '__main__':
    flight_app.run(debug=True)