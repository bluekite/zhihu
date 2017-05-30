
from basic import *



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_questions(configs, headers):

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


def follow_question(configs, headers, q_id):
    url = configs["api"]["prefix"] + "questions/" + str(q_id) + "followers"
    result = requests.post(url, headers=headers)
    sleep_time = random.uniform(2, 4)
    return result

def unfollow_question(configs, headers, q_id):
    url = configs["api"]["prefix"] + "questions/" + str(q_id) + "/followers"
    print(url)
    result = requests.delete(url, headers=headers)
    sleep_time = random.uniform(2, 4)
    print(result, "wait %.1f" %sleep_time, "seconds")
    time.sleep(sleep_time)
    return result

question_file = "../data/questions.json"

def all_questions(configs, headers):
    questions = get_questions(configs, headers)
    questions_ids = [question["id"] for question in questions]
    # pretty_print(questions)
    write_list(questions_ids, question_file)
    print(questions_ids, len(questions_ids))


def del_all_questions(configs, headers):
    question_ids = read_list(question_file)
    for q_id in question_ids:
        unfollow_question(configs,headers, q_id)
    return


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# initial
configs = get_configs()
headers = get_headers(configs)

all_questions(configs, headers)
del_all_questions(configs, headers)
