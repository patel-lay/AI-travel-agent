from parse_request import ParseEssentials
from flask import Flask, request, jsonify
from flask_cors import CORS


flight_app = Flask(__name__)
CORS(flight_app)  # Allow cross-origin requests from any domain


@flight_app.route('/extract-flight-info', methods=['POST'])
def extract_flight_info():
    data = request.json
    user_input = data.get("text", "")

    flight_info  = ParseEssentials()
    flight_info.get_flight_info(user_input)

    print(flight_info.date)
    print(flight_info.src)
    print(flight_info.dst)
    return jsonify(flight_info.date)


if __name__ == '__main__':
    flight_app.run(debug=True)