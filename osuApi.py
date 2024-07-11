import os
import requests
from dotenv import load_dotenv

load_dotenv()
OSU_API_KEY = os.getenv('OSU_API_KEY')


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
