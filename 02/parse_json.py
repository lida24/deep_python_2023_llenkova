import json


counter = {}


def keywords_counter(keyword):
    if keyword not in counter:
        counter[keyword] = 1
    else:
        counter[keyword] += 1
    return counter


def parse_json(
    json_str: str, required_fields=None, keywords=None, keyword_callback=None
):
    if required_fields is None:
        raise ValueError("required_fields parameter is required")
    if keywords is None:
        raise ValueError("keywords parameter is required")
    if keyword_callback is None:
        raise ValueError("keyword_callback parameter is required")
    json_doc = json.loads(json_str)
    for field in required_fields:
        if field in json_doc:
            keywords_list = json_doc[field].split()
            for keyword in set(keywords):
                if keyword.lower() in [kw.lower() for kw in keywords_list]:
                    keyword_callback(keyword)
