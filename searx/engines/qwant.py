"""
 Qwant (Web)

 @website     https://qwant.com/
 @provide-api not officially (https://api.qwant.com/api/search/)

 @using-api   yes
 @results     JSON
 @stable      yes
 @parse       url, title, content
"""

from urllib import urlencode
from json import loads

# engine dependent config
categories = ['general']
paging = True
language_support = True

# search-url
url = 'https://api.qwant.com/api/search/web?count=10&offset={offset}&f=&{query}'


# do search-request
def request(query, params):
    offset = (params['pageno'] - 1) * 10

    params['url'] = url.format(query=urlencode({'q': query}),
                               offset=offset)

    # add language tag if specified
    if params['language'] != 'all':
        params['url'] += '&locale=' + params['language'].lower()

    return params


# get response from search-request
def response(resp):
    results = []

    search_results = loads(resp.text)

    # return empty array if there are no results
    if 'data' not in search_results:
        return []

    data = search_results.get('data', {})

    res = data.get('result', {})

    # parse results
    for result in res.get('items', {}):

        title = result['title']
        res_url = result['url']
        content = result['desc']

        # append result
        results.append({'title': title,
                        'content': content,
                        'url': res_url})

    # return results
    return results
