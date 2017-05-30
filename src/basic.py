# parse
import json
import urllib
# util
import time
import random
# 3rd-party
import requests
from bs4 import BeautifulSoup



"""
    util
"""
def pretty_print(parsed_json):
    print(json.dumps(parsed_json, indent = 4, sort_keys = True))

def write_list(data_list, filename):
    with open(filename, "w") as data_file:
        json.dump(data_list, data_file)
    return

def read_list(filename):
    with open(filename) as data_file:
        data_list = json.load(data_file)
    return data_list

def wait_a_while():
    sleep_time = random.uniform(2, 4)
    print(" Going to wait %.2f" %sleep_time, "seconds")
    time.sleep(sleep_time)
    return sleep_time

"""
    configs
        -
"""
def get_configs():
    configs = {}
    with open("../configs/auth.json") as file:
        configs["auth"] = json.load(file)
    with open("../configs/api.json") as file:
        configs["api"] = json.load(file)
    return configs


def get_headers(configs):
    # zhuanlan's host differ
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, compress, sdch",
        # "Host": "www.zhihu.com",
        # "Origin": "http://www.zhihu.com",
        # "Referer": "http://www.zhihu.com/",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest"
    }

    headers["authorization"] = configs["auth"]["authorization"]
    headers["Cookie"] = configs["auth"]["Cookie"]
    headers["X-Xsrftoken"] = configs["auth"]["X-Xsrftoken"]

    return headers



def get_url(configs, location):
    url = configs["api"]["prefix"] + configs["api"][location]
    return url


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_data(url, params, headers):
    result_raw =  requests.get(url, params=params, headers=headers)
    result_json = json.loads(result_raw.text)
    wait_a_while()
    return result_json

def post_data(url, data, headers):
    result_raw = requests.post(url, data=data, headers=headers)
    wait_a_while()
    return result_raw

def put_data(url, data, headers):
    result_raw = requests.put(url, data=data, headers=headers)
    wait_a_while()
    return result_raw

def get_html(url, headers):
    result_raw  = requests.get(url, headers=headers)
    wait_a_while()
    return result_raw.text


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
