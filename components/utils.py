import requests
from .exceptions import ExternalApiFailedException


def fetch_all_records(api_url):
    all_records = []
    next = api_url
    while next:
        data = call_api(next)
        all_records.extend(data.get("results", []))
        next = data.get("next")
    return all_records


def call_api(api_url):
    try:
        data = requests.get(api_url).json()
    except requests.exceptions.ConnectionError:
        raise ExternalApiFailedException(
            "Connection Error happened while fetching data"
        )
    else:
        return data
