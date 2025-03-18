import ollama
import json


class ParseEssentials():
    
    def __init__(self):
        self.date = ''
        self.src = ''
        self.dst = ''
    
    def get_flight_info(self, user_input):
        prompt = f"""
        You are the AI travel expert. 
        Extract the following details from the text:
        - From
        - To
        - Date
        Put the query in dictionary formatx

        Text: "{user_input}"
        Output:
            - Only output the generated result with the corresponding generated question. The query should only be the raw query nothing else. Do not include any
                headers for the details
                """

        
        response = ollama.chat(model='llama3.2', messages=[{"role": "user", "content": prompt}])
        print(response)

        try:
            # flight_info = {}
            flight_info = json.loads(response['message']['content'])  # Convert to JSON.
            print(flight_info)
            # list_of_strings = self.convert_string_to_dict(flight_info)
            # print(list_of_strings)

            # print(resp)
            # flight_info = {}
            # flight_info = [json.loads(resp)
            # for d in self.extract_between_tags("json", flight_info)
            # ]
            # flight_info = dict(flight_info)
            self.date = flight_info['Date']
            self.src = flight_info['From']
            self.dst = flight_info['To']
            return 
        except json.JSONDecodeError:
            return {"error": "Unable to find the flight details"}
        return



