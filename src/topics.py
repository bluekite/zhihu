
from basic import *


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_topics(configs, headers):

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


topic_file = "../data/topic.json"

def all_topics(configs, headers):
    topics = get_topics(configs, headers)
    topic_ids = [topic["topic"]["id"] for topic in topics]
    pretty_print(topics)
    print(topic_ids, len(topic_ids))
    write_list(topic_ids, topic_file)
    return topics

def follow_unfollow_topic(configs, headers, method, topic_id):

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

def unfollow_all_topics(configs, headers):
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
        follow_unfollow_topic(configs, headers, "unfollow_topic", dest_id)
    return


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# initial
configs = get_configs()
headers = get_headers(configs)

all_topics(configs, headers)
unfollow_all_topics(configs, headers)
