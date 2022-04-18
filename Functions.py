import uuid
import time
import json
import hmac
import hashlib
import base64
from hashlib import sha256
import requests
from Crypto.Hash import HMAC, SHA256

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

def createPayment(amount, name, phone_number, email, address, city, postalCode, country, card_number, security_code, expiry_month, expiry_year):
    url = "https://prod.emea.api.fiservapps.com/sandbox/ipp/payments-gateway/v2/payments/"
    payload ={
        "transactionAmount": {
            "total": amount,
            "currency": "USD"
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



    r =  requests.post(url, data=payload, headers=headers)
    print(r.json())
    r1 = retrievePaymentStatus(r.json()['ipgTransactionId'])


    return r.json()['transactionStatus']

#createPayment(amount="12.23",address="123/3,AndersonRoad",phone_number="94773753001",card_number="4761739001010010",expiry_month="10", expiry_year="22",postalCode="10350",security_code="002",country="USA",email="aarthifnawaz@gmail.com", city="Colombo", name="Aarthif")



