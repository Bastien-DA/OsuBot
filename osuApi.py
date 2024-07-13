import os
import requests
from dotenv import load_dotenv

load_dotenv()
OSU_API_KEY = os.getenv('OSU_API_KEY')


info_compare = {
    "count300": 0,
    "better_count300": "",
    "count100": 0,
    "better_count100": "",
    "count50": 0,
    "better_count50": "",
    "ranked_score": 0,
    "better_ranked_score": "",
    "total_score": 0,
    "better_total_score": "",
    "pp_rank": 0,
    "better_pp_rank": "",
    "level": 0.0,
    "better_level": "",
    "pp_raw": 0.0,
    "better_pp_raw": "",
    "accuracy": 0.0,
    "better_accuracy": "",
    "count_rank_ss": 0,
    "better_count_rank_ss": "",
    "count_rank_s": 0,
    "better_count_rank_s": "",
    "count_rank_a": 0,
    "better_count_rank_a": "",
    "pp_country_rank": 0,
    "better_pp_country_rank": ""
}


def get_user(username: str):
    get_best_response = requests.get(f'https://osu.ppy.sh/api/get_user_best?k={OSU_API_KEY}&u={username}&limit=1')
    get_user_response = requests.get(f'https://osu.ppy.sh/api/get_user?k={OSU_API_KEY}&u={username}')
    if not get_user_response.json() or not get_best_response.json():
        return "User not found", None, None
    get_beatmap_response = requests.get(f'https://osu.ppy.sh/api/get_beatmaps?k={OSU_API_KEY}&b={get_best_response.json()[0]["beatmap_id"]}')
    user_info = get_user_response.json()
    get_best = get_best_response.json()
    get_beatmap = get_beatmap_response.json()
    return user_info[0], get_best[0], get_beatmap[0]


def compare(username1: str, username2: str):
    data_user = requests.get(f'https://osu.ppy.sh/api/get_user?k={OSU_API_KEY}&u={username1}').json()[0]
    data_user2 = requests.get(f'https://osu.ppy.sh/api/get_user?k={OSU_API_KEY}&u={username2}').json()[0]
    keys_int = ['count300', 'count100', 'count50', 'ranked_score', 'total_score', 'pp_rank',
                'count_rank_ss', 'count_rank_s', 'count_rank_a']
    rank_keys = ['pp_rank', 'pp_country_rank']
    keys_float = ['level', 'pp_raw', 'accuracy']
    for key in keys_int:
        data_user[key] = int(data_user[key])
        data_user2[key] = int(data_user2[key])
        if data_user[key] > data_user2[key]:
            info_compare[key] = data_user[key] - data_user2[key]
            info_compare['better_' + key] = data_user['username']
        else:
            info_compare[key] = data_user2[key] - data_user[key]
            info_compare['better_' + key] = data_user2['username']
    for key in rank_keys:
        data_user[key] = int(data_user[key])
        data_user2[key] = int(data_user2[key])
        if data_user[key] < data_user2[key]:
            info_compare[key] = data_user[key]
            info_compare['better_' + key] = data_user['username']
        else:
            info_compare[key] = data_user2[key]
            info_compare['better_' + key] = data_user2['username']
    for key in keys_float:
        data_user[key] = float(data_user[key])
        data_user2[key] = float(data_user2[key])
        if data_user[key] > data_user2[key]:
            info_compare[key] = round(data_user[key] - data_user2[key], 2)
            info_compare['better_' + key] = data_user['username']
        else:
            info_compare[key] = round(data_user2[key] - data_user[key], 2)
            info_compare['better_' + key] = data_user2['username']
    return data_user, data_user2, info_compare


print(compare("guervus", "wanaps"))
