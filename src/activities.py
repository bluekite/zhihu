from basic import *

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_activities(configs, headers):

    url = "https://www.zhihu.com/people/peredaviddeer/activities"
    activities_html = get_html(url, headers=headers)
    soup = BeautifulSoup(activities_html, "html.parser")
    raw_text = soup.find_all(attrs={"data-reactid": "20"})[0]["data-state"]
    next_url = raw_text.split("\"next\":\"")[1].split("\"}}")[0]

    print(next_url)
    # "http://www.zhihu.com/api/v4/members/peredaviddeer/activities?limit=20&after_id=1495543641&desktop=True"

    params = {
        "limit": 20,
        "desktop": True
    }

    activities = []
    result_json = get_data(next_url, {}, headers)

    activities += result_json["data"]
    is_end = result_json["paging"]["is_end"]


    while not is_end:
        url = configs["api"]["activities"]
        result_json = get_data(url, params, headers)
        activities += result_json["data"]
        params["after_id"] = result_json["data"][-1]["id"]
        is_end = result_json["paging"]["is_end"]
        print(len(activities))

    return activities

activities_file = "../data/activities.json"



# voted passages answers
def all_voted(configs, headers):
    activities = get_activities(configs, headers)
    pretty_print(activities)
    answers_ids = [(activity["target"]["id"], activity["verb"]) \
                                for activity in activities]
    write_list(answers_ids, activities_file)
    print(answers_ids, len(answers_ids))


# zhuanlan: PUT https://zhuanlan.zhihu.com/api/posts/24984209/rating
# {value: "none"}  {value: "like"}
# MEMBER_VOTEUP_ARTICLE
def unvote_article(configs, headers, a_id):
    url = "https://zhuanlan.zhihu.com/api/posts/" + \
            str(a_id) + "/rating"
    data = {"value": "none"}
    result = put_data(url, json.dumps(data), headers)
    return result

# answer: POST https://www.zhihu.com/api/v4/answers/58478660/voters
# {type: "neutral"}  {type: "up"}
# ANSWER_VOTE_UP
def unvote_answer(configs, headers, a_id):
    url = "https://www.zhihu.com/api/v4/answers/" + \
            str(a_id) + "/voters"
    data = {"type": "neutral"}
    result = post_data(url, json.dumps(data), headers)
    return result

def unvote_all(configs, headers):
    activity_ids = read_list(activities_file)
    for a_id in activity_ids:
        if a_id[1] == "MEMBER_VOTEUP_ARTICLE":
            result = unvote_article(configs, headers, a_id[0])
        if a_id[1] == "ANSWER_VOTE_UP":
            result =  unvote_answer(configs, headers, a_id[0])
        print(result, result.text)
    return


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# initial
configs = get_configs()
headers = get_headers(configs)


unvote_all(configs, headers)
