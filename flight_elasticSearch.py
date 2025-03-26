from elasticsearch import Elasticsearch, helpers

ELASTIC_URL = "https://localhost:9200"
CA_CERT_PATH = "/Users/laypatel/http_ca.crt"
USERNAME = "elastic"
PASSWORD = "e=daqTKy20DDhAjCgFMx"


es = Elasticsearch(
        ELASTIC_URL,
        ca_certs=CA_CERT_PATH,
        basic_auth=(USERNAME, PASSWORD)
    )

index_name = "flights"
index_mapping = {
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "leave_date": { "type": "date", "format": "MMMM d" },
      "return_date": { "type": "date", "format": "MMMM d" },
      "depart_time_leg1": { "type": "keyword" },
      "arrival_time_leg1": { "type": "keyword" },
      "emission_avg_diff": { "type": "integer" },
      "price": { "type": "float" },
      "trip_type": { "type": "keyword" },
      "access_date": { "type": "date", "format": "yyyy-MM-dd" }
    }
  }
}
# Paste the JSON mapping here
def create_index():
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_mapping)
    else:
        print("Entry already exists")
   

def generate_bulk_data(data):
    for flight in data:
        yield {
            "_index": index_name,
            "_source": {
                "leave_date": flight["Leave Date"],
                "return_date": flight.get("Return Date", None),  # Handle None values
                "depart_time_leg1": flight["Depart Time (Leg 1)"],
                "arrival_time_leg1": flight["Arrival Time (Leg 1)"],
                "emission_avg_diff": flight["Emission Avg Diff (%)"],
                "price": flight["Price ($)"],
                "trip_type": flight["Trip Type"],
                "access_date": flight["Access Date"]
            }
        }
def insert_data(flights_data):
    try: 
        response = helpers.bulk(es, generate_bulk_data(flights_data))
        print("Bulk insert completed:", response)
    except Exception as e:
        print("Error inserting data:", e)

def query():
    query = {
    "query": {
        "range": {
            "price": {"lt": 350}  # "lt" means "less than"
            }   
        }
    }

    # Execute search
    response = es.search(index=index_name, body=query)

    # Print results
    for hit in response["hits"]["hits"]:
        return hit["_source"]
    
    return "No response found"