import requests
from django.conf import settings
from datetime import datetime
import base64

# Get M-Pesa access token
def get_mpesa_token():
    api_url= f"{settings.MPESA_LIPA_NG_NG_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    # api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials' if settings.MPESA_ENVIRONMENT == 'sandbox' else 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}'.encode()).decode('utf-8'),
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    json_response = response.json()
    return json_response['access_token']

# Initiate an M-Pesa payment
def initiate_payment(amount, phone_number):
     
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest' if settings.MPESA_ENVIRONMENT == 'sandbox' else 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    access_token = get_mpesa_token()
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    payload = {
        'BusinessShortCode': settings.MPESA_LIPA_SHORTCODE,
        'Password': base64.b64encode(f'{settings.MPESA_LIPA_SHORTCODE}{settings.MPESA_LIPA_PASSKEY}{datetime.now().strftime("%Y%m%d%H%M%S")}'.encode()).decode('utf-8'),
        'Timestamp': datetime.now().strftime("%Y%m%d%H%M%S"),
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': settings.MPESA_LIPA_SHORTCODE,
        'PhoneNumber': phone_number,
        'CallBackURL': 'https://yourdomain.com/callback',
        'AccountReference': 'Test123',
        'TransactionDesc': 'Payment for testing'
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
