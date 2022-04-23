import uuid
import time
import json
import hmac
import hashlib
import base64
from hashlib import sha256
import requests
from Crypto.Hash import HMAC, SHA256

def retrieveTransactionStatus(id):
    print(id)
    api_key = "sD1pPsnDa7wExgyKt30yu5AfgiiIBBYB"
    url = f"https://prod.emea.api.fiservapps.com/sandbox/exp/v1/transactions"

    headers = {
        'Content-Type': "application/json",
        'Api-Key': api_key,
        'Merchant-Id': '881111110000228'
    }
    r = requests.get(url, headers=headers)
    print(r.json())

def retrievePaymentStatus(id):
    api_key = "sD1pPsnDa7wExgyKt30yu5AfgiiIBBYB"
    secret_key = "XTEoOx4D09cg8DbMW8LU57ZwZ6qCGRgh5mGMS3OBd8v"
    client_request = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))

    raw_signature = '{}{}{}'.format(api_key, client_request, timestamp)
    print(raw_signature)

    signature = hmac.new(secret_key.encode(), raw_signature.encode(), hashlib.sha256).digest()
    b64_sig = base64.b64encode(signature).decode()
    print(b64_sig)

    headers = {
        "Client-Request-Id": client_request,
        "Api-Key": api_key,
        "Timestamp": timestamp,
        "Message-Signature": b64_sig
    }
    url = f'https://prod.emea.api.fiservapps.com/sandbox/ipp/payments-gateway/v2/payments/{id}'
    r = requests.get(url=url, headers=headers)
    return r.json()

def createPayment(currency, amount, name, phone_number, email, address, city, postalCode, country, card_number, security_code, expiry_month, expiry_year, description):
    url = "https://prod.emea.api.fiservapps.com/sandbox/ipp/payments-gateway/v2/payments/"
    payload ={
        "transactionAmount": {
            "total": amount,
            "currency": currency
        },
        "requestType": "PaymentCardCreditTransaction",
        "paymentMethod": {
            "paymentCard": {
                "number": card_number,
                "securityCode": security_code,
                "expiryDate": {
                    "month": expiry_month,
                    "year": expiry_year
                }
            }
        },
        "order" : {
            "billing" : {
                "name" : name,
                "contact" : {
                    "phone" : phone_number,
                    "email" : email
                },
                "address" : {
                    "address1" : address,
                    "city" : city,
                    "postalCode": postalCode,
                    "country" : country
                }
            },

            "additionalDetails" : {
                "comments" : description
            }
        }
    }
    payload = json.dumps(payload)
    payload = str(payload)
    api_key = "sD1pPsnDa7wExgyKt30yu5AfgiiIBBYB"
    secret_key = "XTEoOx4D09cg8DbMW8LU57ZwZ6qCGRgh5mGMS3OBd8v"
    client_request = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))

    raw_signature = '{}{}{}{}'.format(api_key, client_request, timestamp, str(payload))
    print(raw_signature)

    signature = hmac.new(secret_key.encode(), raw_signature.encode(), hashlib.sha256).digest()
    b64_sig = base64.b64encode(signature).decode()
    print(b64_sig)


    headers = {
        "Client-Request-Id": client_request,
        "Api-Key": api_key,
        "Timestamp": timestamp,
        "Message-Signature": b64_sig
    }


    try:
        r =  requests.post(url, data=payload, headers=headers)
        print(r.json())
        retrieveTransactionStatus(r.json()['ipgTransactionId'])
        #retrievePaymentStatus(r.json()['ipgTransactionId'])

        return r.json()['transactionStatus']
    except Exception as e:
        return "An Error Occurred, Please Try Again with valid details"

#createPayment(amount="12.23",address="123/3,AndersonRoad",phone_number="94773753001",card_number="4761739001010010",expiry_month="10", expiry_year="22",postalCode="10350",security_code="002",country="USA",email="aarthifnawaz@gmail.com", city="Colombo", name="Aarthif")



