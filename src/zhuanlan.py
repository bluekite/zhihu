from basic import *

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def get_zhuanlans(configs, headers):

    url = get_url(configs, "zhuanlans")
    offset = 0
    limit = 20
    include = "data[*].intro,followers,Carticles_count"
    params = {
        "include" : include,
        "offset" : offset,
        "limit" : limit
    }

    zhuanlans = []

    result_json = get_data(url, params, headers)
    zhuanlans += result_json["data"]
    totals = result_json["paging"]["totals"]

    while offset < totals:
        offset += limit
        params["offset"] = offset
        result_json = get_data(url, params, headers)
        zhuanlans += result_json["data"]
        print(offset)
    return zhuanlans


zhuanlan_file = "../data/zhuanlan.json"
def all_zhuanlans(configs, headers):
    zhuanlans = get_zhuanlans(configs, headers)
    zhuanlan_ids = [zhuanlan["id"] for zhuanlan in zhuanlans]
    print(zhuanlan_ids, len(zhuanlan_ids))
    write_list(zhuanlan_ids, zhuanlan_file)
    return zhuanlans


def unfollow_zhuanlan(configs, headers, z_id):
    url = configs["api"]["prefix"] + "columns/" + str(z_id) + "/followers"
    print(url)
    result = requests.delete(url, headers=headers)
    print(result, result.text)
    wait_a_while()
    return result

"put for follow, delete for unfollow_zhuanlan"
def del_all_zhuanlan(configs, headers):
    zhuanlan_ids = read_list(zhuanlan_file)
    for z_id in zhuanlan_ids:
        result = unfollow_zhuanlan(configs, headers, z_id)
    return

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# initial
configs = get_configs()
headers = get_headers(configs)

all_zhuanlans(configs, headers)
del_all_zhuanlan(configs, headers)
