import ollama
import json

class ParseEssentials():
    
    def __init__(self):
        self.date = 0
        self.src = ''
        self.dst = ''
    
    def get_flight_info(self, user_input):
        prompt = prompt = f"""
        Extract the following details from the text:
        - Departure City (From)
        - Destination City (To)
        - Date of travel

        Text: "{user_input}"

        Respond in JSON format:
        {{"from": "departure city", "to": "destination city", "date": "travel date"}} """

        
        response = ollama.chat(model='llama3.2', messages=[{"role": "user", "content": prompt}])
        print(response)

        try:
            flight_info = json.loads(response['message']['content'])  # Convert to JSON
            print(flight_info)
            self.date = flight_info["date"]
            self.src = flight_info["from"]
            self.dst = flight_info["to"]
            return 
        except json.JSONDecodeError:
            return {"error": "Unable to find the flight details"}
        return 



