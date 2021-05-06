import requests
from functools import wraps
from flask import Blueprint, request, jsonify, Response
from bs4 import BeautifulSoup
import numpy as np

contribute_blueprint = Blueprint('contribute', __name__)


def is_api(required_keys):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request.on_json_loading_failed = lambda: jsonify({'success': False, 'error': 'JSON_parsing_failed'})
            data = request.get_json()
            if not isinstance(data, dict):
                return jsonify({'success': False, 'error': 'dictionary_required'})
            data = {str(k).lower(): v for k, v in data.items()}
            if not set(required_keys).issubset(set(data.keys())):
                return jsonify({'success': False, 'error': 'no_required_args'})
            else:
                ret_data: Response = func(data, *args, **kwargs)
                if isinstance(ret_data, tuple):
                    return jsonify(ret_data[0]), ret_data[1]
                else:
                    return jsonify(ret_data)
        return wrapper
    return decorator


def contribute_calender_crawling(github_id: str):
    try:
        resp = requests.get(f"https://github.com/{github_id}")
    except:
        return False, None

    if resp.status_code != 200:
        return False, None

    day_list = BeautifulSoup(resp.text, 'html.parser').find('g').find_all('rect', 'ContributionCalendar-day')
    data_count = list()

    for day in day_list:
        data_count.append({'data-count': int(day.get('data-count')), 'data-date': day.get('data-date')})
    print(data_count)
    return data_count


@contribute_blueprint.route('/<string:github_id>', methods=['GET'])
def get_contribute(github_id):
    return jsonify(contribute_calender_crawling(github_id))
