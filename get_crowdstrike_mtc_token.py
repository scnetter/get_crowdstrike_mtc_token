import os
from dotenv import load_dotenv
import sys
import requests

load_dotenv()

## TODO: Add usage for Mac - remainder of script will work the same.

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
    print("\n##To get the device ID, on the target host run one of the commands below based on your operating system.##")
    print("Windows:")
    print(" reg query HKLM\\System\\CurrentControlSet\\services\\CSAgent\\Sim\\ /f AG")
    print("MacOS:")
    print(" sudo /Applications/Falcon.app/Contents/Resources/falconctl stats | grep agentID")
    print("Linux:")
    print(" sudo /opt/CrowdStrike/falconctl -g --aid")
    print("\nThe device id is the value returned. It will be listed as 'aid', agentID or AG depending on the system.")
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

    if response.status_code not in [200, 201]:
        print(f"Error: Authentication failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)

    token = response.json()['access_token']

    if not token:
        print("Error: No token returned in response")
        exit(1)
    
    print(f"Authentication successful.")
    return token

# Get the MTC token

def get_mtc_token(device_id, auth_token, base_url):
    """ 
    Get the MTC token for a given device ID from the Crowdstrike API
    """
    token_url = f"{base_url}/policy/combined/reveal-uninstall-token/v1"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    payload = {
        'audit_message': f"Generating MTC token for device {device_id}",
        'device_id': device_id,
    }

    response = requests.post(token_url, headers=headers, json=payload)

    if response.status_code not in [200, 201]:
        print(f"Error: Token request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)

    response_data = response.json()

    # Extract the uninstall token from the resources array
    if response_data.get('resources') and len(response_data['resources']) > 0:
        uninstall_token = response_data['resources'][0].get('uninstall_token')
        if uninstall_token:
            print("MTC Token generated successfully")
            return uninstall_token
        else:
            print("Error: No uninstall token found in response")
            print(f"Response: {response_data}")
            exit(1)

# Test authentication
auth_token = get_auth_token(client_id, client_secret, base_url)
print(f"✓ BearerToken received: {auth_token[:20]}...")  # Print first 20 chars so we don't expose the full token

# Get the MTC token
mtc_token = get_mtc_token(device_id, auth_token, base_url)
print(f"✓ MTC token received: {mtc_token}") 