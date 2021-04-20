from requests import get
from os import getenv


def verify_server(token, base_url, group_id, server_id):
    response = get(
        'https://api.vk.com/method/groups.editCallbackServer',
        params={
            'group_id': group_id,
            'access_token': token,
            'v': '5.130',
            'url': base_url + '/api/v2/bot/',
            'title': 'SESC MATE',
            'secret_key': getenv('SECRET_KEY', 'PAPAZPAPAZ'),
            'server_id': server_id
        }
    )

    return response.json()
