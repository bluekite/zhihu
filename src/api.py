
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
    data
"""
question_file = "../data/questions.json"
topic_file = "../data/topic.json"

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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, compress, sdch",
        "Host": "www.zhihu.com",
        "Origin": "http://www.zhihu.com",
        "Referer": "http://www.zhihu.com/",
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
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# initial
configs = get_configs()
headers = get_headers(configs)


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

def get_html(url, headers=headers):
    result_raw  = requests.get(url, headers=headers)
    wait_a_while()
    return result_raw.text
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_topics(configs):

    url = get_url(configs, "topics")
    offset = 0
    limit = 20
    # include = "data[*].topic.introduction"
    include = "data[*]"
    params = {
        "include" : include,
        "offset" : offset,
        "limit" : limit
    }

    topics = []

    result_json = get_data(url, params, headers)
    topics += result_json["data"]

    totals = result_json["paging"]["totals"]

    while offset < totals:
        offset += limit
        params["offset"] = offset
        result_json = get_data(url, params, headers)
        topics += result_json["data"]
        print(offset)
    return topics

def all_topics(configs):
    topics = get_topics(configs)
    topic_ids = [topic["topic"]["id"] for topic in topics]
    pretty_print(topics)
    print(topic_ids, len(topic_ids))
    write_list(topic_ids, topic_file)
    return topics

def follow_unfollow_topic(configs, method, topic_id):

    url = configs["api"]["topics_follow"]

    headers = get_headers(configs)

    data = {
        "_xsrf": configs["auth"]["X-Xsrftoken"],
        "method": method,
        "params": json.dumps({"topic_id": topic_id})
    }

    result = post_data(url, data, headers)
    print(method, " ",result)
    return result

def unfollow_all_topics(configs):
    topic_ids = read_list(topic_file)
    url = ""
    for topic_id in topic_ids:
        url = "https://www.zhihu.com/topic/" + str(topic_id) + "/hot"
        print(url)
        topic_html = get_html(url, headers=headers)
        soup = BeautifulSoup(topic_html, "html.parser")
        dest_input = soup.find(class_="zg-mr10")
        dest_id = int(dest_input.get("id")[3:])
        print("topic true id: ", dest_id)
        follow_unfollow_topic(configs, "unfollow_topic", dest_id)
    return

all_topics(configs)
unfollow_all_topics(configs)




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_questions(configs):

    url = get_url(configs, "questions")

    include="data[*].created,answer_count,follower_count,author"
    offset = 0
    limit = 20
    params = {
        "include" : include,
        "offset" : offset,
        "limit" : limit
    }

    questions = []
    result_json = get_data(url, params, headers)

    questions += result_json["data"]
    totals = result_json["paging"]["totals"]
    print("totals %d" %totals)

    while offset < totals:
        offset += limit
        params["offset"] = offset
        result_json = get_data(url, params, headers)
        questions += result_json["data"]
        print(len(questions))
    return questions


def follow_question(configs, q_id):
    url = configs["api"]["prefix"] + "questions/" + str(q_id) + "followers"
    result = requests.post(url, headers=headers)
    return result

def unfollow_question(configs, q_id):
    url = configs["api"]["prefix"] + "questions/" + str(q_id) + "/followers"
    print(url)
    result = requests.delete(url, headers=headers)
    sleep_time = random.uniform(2, 4)
    print(result, "wait %.1f" %sleep_time, "seconds")
    time.sleep(sleep_time)
    return result

def all_questions(configs):
    questions = get_questions(configs)
    questions_ids = [question["id"] for question in questions]
    # pretty_print(questions)
    write_list(questions_ids, question_file)
    print(questions_ids, len(questions_ids))


def del_all_questions(configs):
    question_ids = read_list(question_file)
    for q_id in question_ids:
        unfollow_question(configs, q_id)
    return


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" for test "
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
