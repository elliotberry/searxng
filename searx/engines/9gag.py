# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
# pylint: disable=invalid-name
"""9GAG (social media)"""

from json import loads
from datetime import datetime
from urllib.parse import urlencode

about = {
    "website": 'https://9gag.com/',
    "wikidata_id": 'Q277421',
    "official_api_documentation": None,
    "use_official_api": True,
    "require_api_key": False,
    "results": 'JSON',
}

categories = ['social media']
paging = True

search_url = "https://9gag.com/v1/search-posts?{query}"
page_size = 10


def request(query, params):
    query = urlencode({'query': query, 'c': (params['pageno'] - 1) * page_size})

    params['url'] = search_url.format(query=query)

    return params


def response(resp):
    results = []

    json_results = loads(resp.text)['data']['posts']

    for result in json_results:
        result_type = result['type']

        if result_type == 'Photo':
            results.append(
                {
                    'template': 'images.html',
                    'url': result['url'],
                    'title': result['title'],
                    'content': result['description'],
                    'publishedDate': datetime.utcfromtimestamp(result['creationTs']),
                    'img_src': result['images']['image700']['url'],
                    'thumbnail_src': result['images']['imageFbThumbnail']['url'],
                }
            )
        elif result_type == 'Animated':
            results.append(
                {
                    'template': 'videos.html',
                    'url': result['url'],
                    'title': result['title'],
                    'content': result['description'],
                    'publishedDate': datetime.utcfromtimestamp(result['creationTs']),
                    'thumbnail': result['images']['imageFbThumbnail']['url'],
                }
            )

    return results
