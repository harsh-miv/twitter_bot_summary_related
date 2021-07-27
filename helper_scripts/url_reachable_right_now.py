import requests
import re

def is_url_currently_reachable(url):
    r=requests.get(url)
    status_code=str(r.status_code)

    if re.search("4..",status_code) or re.search("5..",status_code):
        return False

    return True
