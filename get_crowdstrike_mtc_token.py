import os
from dotenv import load_dotenv
import sys
import requests

load_dotenv()

# Load API credentials from environment variables
client_id = os.getenv('CROWDSTRIKE_CLIENT_ID')
client_secret = os.getenv('CROWDSTRIKE_CLIENT_SECRET')
base_url = os.getenv('CROWDSTRIKE_BASE_URL')

# validate the environment variables
if not all([client_id, client_secret, base_url]):
    print("Error: Missing required environment variables")
    print(f"  CROWDSTRIKE_CLIENT_ID: {bool(client_id)}")
    print(f"  CROWDSTRIKE_CLIENT_SECRET: {bool(client_secret)}")
    print(f"  CROWDSTRIKE_BASE_URL: {bool(base_url)}")
    exit(1)

print(" All credentials loaded successfully")

# Get device_id from command line arguments
if len(sys.argv) < 2:
    print("Error: Device ID is required")
    print("\nUsage: python get_crowdstrike_mtc_token.py <device_id>")
    print("\nTo get the device ID, on the target host run:")
    print(" reg query HKLM\\System\\CurrentControlSet\\services\\CSAgent\\Sim\\ /f AG")
    print("\nThe device id is the value returned from the registry query")
    exit(1)

device_id = sys.argv[1]
print(f"Device ID: {device_id}")

# Get the initial Oauth2 token
def get_auth_token(client_id, client_secret, base_url):
    """
    Autneticate with Crowdstrike API and return the bearer token
    """
    auth_url = f"{base_url}/oauth2/token"

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }

    response = requests.post(auth_url, data=payload)

    if response.status_code != 200:
        print(f"Error: Authentication failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)

    token = response.json()['access_token']

    if not token:
        print("Error: No token returned in response")
        exit(1)
    
    print(f"Authentication successful.")
    return token

