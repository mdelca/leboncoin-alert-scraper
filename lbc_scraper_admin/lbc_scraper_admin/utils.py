from collections import namedtuple

import requests

Result = namedtuple('Result', ['is_valid', 'message'])


def check_url(url):
    """
    Vérifie que l'URL est bien une URL leboncoin et qu'elle correspond bien à une recherche valide
    """
    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema:
        result = Result(is_valid=False, message="Ceci n'est pas une url valide")

    if 'www.leboncoin.fr' not in url:
        result = Result(is_valid=False, message="Ceci n'est pas une url leboncoin")
    elif response.url is 'https://www.leboncoin.fr/' or not response.ok:
        result = Result(is_valid=False, message="La recherche n'est pas valide")
    else:
        result = Result(is_valid=True, message=None)

    return result
