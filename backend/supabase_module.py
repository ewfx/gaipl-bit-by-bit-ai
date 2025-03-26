from supabase import create_client, Client
import json
from dotenv import load_dotenv
load_dotenv()
import os
SUPABASE_URL = "https://hmnuhtoapsyaiakvnmbu.supabase.co"  # Replace with your Supabase URL
SUPABASE_KEY = os.getenv("SUPABASE_KEY") # Use service role key if you need write access

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
bucket_name = "bitbybitbackenddata"

def return_CI_data():
    file_path = "CI-data.json"  # Adjust the path as per your storage setup
    # Get public URL (if file is publicly accessible)
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
    # print("Public URL:", public_url)
    response = supabase.storage.from_(bucket_name).download(file_path)
    json_data = json.loads(response)
    # print(json_data)
    return json_data

def return_servicenow_data():
    file_path = "servicenow.json"  # Adjust the path as per your storage setup
    # Get public URL (if file is publicly accessible)
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
    # print("Public URL:", public_url)
    response = supabase.storage.from_(bucket_name).download(file_path)
    json_data = json.loads(response)
    # print(json_data)
    return json_data

def return_grafana_data():
    file_path = "grafana-data.json"  # Adjust the path as per your storage setup
    # Get public URL (if file is publicly accessible)
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
    # print("Public URL:", public_url)
    response = supabase.storage.from_(bucket_name).download(file_path)
    json_data = json.loads(response)
    # print(json_data)
    return json_data

def update_supabase_data(file_path,updated_json_bytes):
    supabase.storage.from_(bucket_name).remove([file_path])
    supabase.storage.from_(bucket_name).upload(file_path, updated_json_bytes, file_options={"content-type": "application/json"})

def return_supabase_env_keys():
    file_path = "token_access.json"  # Adjust the path as per your storage setup
    # Get public URL (if file is publicly accessible)
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
    # print("Public URL:", public_url)
    response = supabase.storage.from_(bucket_name).download(file_path)
    json_data = json.loads(response)
    # print(json_data)
    return json_data