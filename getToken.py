import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# IMPORTANT: You must replace this code every time you run the script via the browser URL.
# If you get an error, this code is likely expired or already used.
code_from_url = '' 

def exchange_code_for_token():
    """
    Exchanges the temporary authorization code for a permanent refresh token
    and a temporary access token.
    """
    
    # Strava OAuth2 token URL
    url = "https://www.strava.com/oauth/token"
    
    # Payload data for the POST request
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code_from_url,
        'grant_type': 'authorization_code'
    }
    
    print("--- Requesting Token from Strava ---")
    
    try:
        # Make the POST request
        response = requests.post(url, data=payload)
        data = response.json()
        
        # Check if the request was successful (HTTP 200)
        if response.status_code == 200:
            print("\n--- SUCCESS! ---")
            print(f"ACCESS TOKEN: {data['access_token']}")
            print(f"REFRESH TOKEN: {data['refresh_token']}")
            print(f"EXPIRES AT: {data['expires_at']}")
            print("\n-> SAVE the 'refresh_token'. You will use it to generate new access tokens automatically in the future.")
            
        else:
            # Handle specific API errors
            print("\n--- ERROR ---")
            print(f"Status Code: {response.status_code}")
            print(f"Error Message: {data}")
            
            if response.status_code == 400:
                print("\n-> TIP: Your 'code' might be expired or already used. Generate a new one in the browser.")
                
    except Exception as e:
        print(f"An error occurred during the request: {e}")

if __name__ == "__main__":
    # Check if the user forgot to update the placeholder
    if code_from_url == 'PEGA_AQUI_TU_NUEVO_CODIGO_DEL_NAVEGADOR':
        print("ERROR: You need to paste a fresh code in the 'code_from_url' variable first.")
    else:
        exchange_code_for_token()