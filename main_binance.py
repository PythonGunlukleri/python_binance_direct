import csv
import json
import random

import requests
from flask import Flask, redirect, request
import hmac
import time
import hashlib
import requests

from urllib.parse import urlencode



KEY = "api_key_binance"
SECRET = "api_secret_binance"

api_key_client = "HA3mkCFEfdjT7lh3aVHXCAiI3uwYX7AO1aheykxble1CZvBLXQ6liYcWzmyD"
api_secret_client = "cYdLHQRJPznV93oBTj3s1R0efUQpbSQvkYs3QIzjhrCkLFHiwG49y4duwUH1"

BASE_URL = "https://api.binance.com"






def check_signature_key(timestamp,signature,test):

    message = f"{timestamp}{test}"
    signaturee = hashingg(message, test)
    print(signaturee,signature)
    if signature == signaturee:
        return True

def hashing(query_string):
    return hmac.new(
        SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

def hashingg(query_string):
    return hmac.new(
        api_secret_client.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY}
    )
    return {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }.get(http_method, "GET")



def send_signed_request(http_method, url_path, payload):
    query_string = urlencode(payload)
    # replace single quote to double quote
    query_string = query_string.replace("%27", "%22")
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
        BASE_URL + url_path + "?" + query_string + "&signature=" + hashing(query_string)
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}
    response = dispatch_request(http_method)(**params)
    return response.json()





def send_public_request(method,url_path, payload):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + "?" + query_string
    print("{}".format(url))
    response = dispatch_request(method)(url=url)
    return response.json()

app = Flask(__name__)

@app.before_request
def log_request():


    print(f"Endpoint: {request.path}, {request.method}")
    endpoint = request.path
    params = request.args
    params = params.to_dict()
    print(params)

    for key in list(params.keys()):
        if params[key] == '':
            del params[key]


    request_method = request.method
    api_key_clientt = request.headers.get('X-MBX-APIKEY')
    try:
        api_secret_clientt = params['signature']
    except:
        pass
    try:
        timestamp = params['timestamp']
    except:
        pass

    try:
        print(api_secret_clientt)
    except:
        api_secret_clientt = None

    try:
        print(timestamp)
    except:
        timestamp = None
    print(type(api_secret_clientt))
    print(type(timestamp))


    if api_secret_clientt is not None:
        if timestamp is not None:

            params.pop('signature', None)


            query_string = urlencode(params).replace("%27", "%22")
            print(query_string)

            checked_signature_secret = hashingg(query_string)
            print(api_secret_clientt, checked_signature_secret)

            if api_key_clientt != api_key_client:
                return "False api key"
            if api_secret_clientt != checked_signature_secret:
                return "False secret key"
            params.pop('timestamp', None)


            print(params)

            response = send_signed_request(request_method, endpoint, params)
    if api_secret_clientt is None:
        if timestamp is None:

            response = send_public_request(request_method,endpoint,params)
    try:
        qwe = response
    except:
        if api_secret_clientt is None:
            return "Signature required"
        if timestamp is None:
            return "Timestamp required"

    son = response
    #print(son)


    return son
















app.run()
