import urllib.parse


def add_url_param(url, params):
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urllib.parse.urlencode(query)

    return urllib.parse.urlunparse(url_parts)


def get_url_param(url, param):
    parsed = urllib.parse.urlparse(url)
    param_dict = urllib.parse.parse_qs(parsed.query)
    if param_dict.get(param):
        return param_dict.get(param)[0]
