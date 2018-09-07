#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by bu on 2018-08-28
"""
from __future__ import unicode_literals
import time
import hashlib
import json as complex_json
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)
http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=1, read=2))


class RequestClient(object):
    __headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    def __init__(self, headers={}):
        self.apikey = ''      	# replace
        self.apisecret = ''     # replace
        self.url = 'https://api.bddfinex.com'
        self.headers = self.__headers
        self.headers.update(headers)

    @staticmethod
    def get_sign(params, appsecret):
        sort_params = sorted(params)
        data = []
        for item in sort_params:
            data.append(item + '=' + str(params[item]))
        str_params = "{0}&apisecret={1}".format('&'.join(data), appsecret)
        token = hashlib.md5(str_params).hexdigest()
        return token

    def set_authorization(self, params):
        params['apikey'] = self.apikey
        params['time'] = int(time.time())
        self.headers['AUTHORIZATION'] = self.get_sign(params, self.apisecret)

    def request(self, method, url, params={}, data='', json={}):
        method = method.upper()
        if method in ['GET', 'DELETE']:
            self.set_authorization(params)
            result = http.request(method, url, fields=params, headers=self.headers)
        else:
            if data:
                json.update(complex_json.loads(data))
            self.set_authorization(json)
            encoded_data = complex_json.dumps(json).encode('utf-8')
            result = http.request(method, url, body=encoded_data, headers=self.headers)
        return result


def get_account():
    request_client = RequestClient()
    response = request_client.request('GET', '{url}/account/balance'.format(url=request_client.url))
    print response.data


def order_list(market_type,state,offset,limit):
    request_client = RequestClient()
    params = {
        'market': market_type,
		'states': state,
		'offset': offset,
		'limit' : limit
    }
    response = request_client.request(
            'GET',
            '{url}/orders/list'.format(url=request_client.url),
            params=params
    )
    print response.data


def put_limit():
    request_client = RequestClient()
    data = {
		"amount": "1",
		"price": "100",
		"side": "sell",
		"type": "limit",
		"market": "ETHUSDT"
	}

    response = request_client.request(
            'GET',
            '{url}/orders/create_order'.format(url=request_client.url),
            params=data,
    )
    return response.data


def put_market():
    request_client = RequestClient()

    data = {
		"amount": "200",
		"side": "sell",
		"type": "limit",
		"market": "ETHUSDT"
	}

    response = request_client.request(
            'GET',
            '{url}/orders/create_order'.format(url=request_client.url),
            params=data,
    )
    print response.data


def cancel_order(id, market):
    request_client = RequestClient()
    data = {
        "order_id": id,
        "market": market,
    }
    print market

    response = request_client.request(
            'GET',
            '{url}/orders/cancel'.format(url=request_client.url),
            params=data,
    )
    print response.data


#get_account()
#order_list("ETHUSDT","filled",0,100)
#print(put_limit())

	
if __name__ == '__main__':
    count = 1
    a = time.time() * 1000
    while True:
        b = time.time() * 1000
        order_data = complex_json.loads(put_limit())['data']
        id = order_data['id']
        market = order_data['market']
        cancel_order(id, market)
        print time.time() * 1000 - b
        count += 1
        if count >= 50:
            break

    print 'avg', (time.time() * 1000 - a) / 50.0
