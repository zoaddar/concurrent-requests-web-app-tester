#!/usr/bin/python3

import requests
import time
from datetime import datetime
import re
import random

def login():
    base_url = 'http://example.com'

    # Login
    url = base_url + '/auth/login'
    payload = {
        'username': 'root',
        'password': 'root',
    }
    # return payload
    res = requests.post(url, data=payload)

    # we need the session cookie
    return res.cookies

def http_test():
    cookies = login()
    # print(cookies)
    # return {}

    base_url = 'http://example.com'

    # generate sales report
    url = base_url + '/reports/sales'

    # need to pass the cookies in order to tell the server that I'm "that" person
    # this is GET request, because need to get the CSRF token before can do a POST
    res = requests.get(url, cookies=cookies)
    html = res.text.encode('utf-8')
    # the "pattern" is depends on how you construct your html page
    pattern = 'name="csrf-token" content="(\w+)"'
    matches = re.findall(pattern, html)
    token = matches[0]

    # POST to generate sales report
    payload = {
        'date': '2016-06-27',
        '_token': token,
        'sales_id': random.randint(1, 30),
    }
    res = requests.post(url, cookies=cookies, data=payload)

def main():
    for i in range(0, 20):
        print(datetime.now())
        http_test()
        time.sleep(1) # every 1 second submit http requests {login, GET report, POST report}
        # print("\n")

if __name__ == "__main__":
    main()
