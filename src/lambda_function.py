import json
from dotenv import dotenv_values
from supabase import create_client

config = dotenv_values(".env")

def lambda_handler(event, context):
    temperature = event.get('temperature', float("NaN"))
    humidity = event.get('humidity', float("NaN"))
    
    db_url = config[ "DB_URL" ]
    db_key = config["DB_KEY"]
    superbase = create_client(db_url, db_key)
    superbase.table('sensor_data').insert({"temperature": temperature, "humidity": humidity}).execute()
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps({"temperature": temperature, "humidity": humidity, "message": "accept" })
    }
