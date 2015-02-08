## Blekko (Images)
#
# @website     https://blekko.com
# @provide-api yes (inofficial)
#
# @using-api   yes
# @results     JSON
# @stable      yes
# @parse       url, title, img_src

from json import loads
from urllib import urlencode

# engine dependent config
categories = ['images']
paging = True

# search-url
base_url = 'https://blekko.com'
search_url = '/api/images?{query}&c={c}'


# do search-request
def request(query, params):
    c = (params['pageno'] - 1) * 48

    params['url'] = base_url +\
        search_url.format(query=urlencode({'q': query}),
                          c=c)

    if params['pageno'] != 1:
        params['url'] += '&page={pageno}'.format(pageno=(params['pageno']-1))

    return params


# get response from search-request
def response(resp):
    results = []

    search_results = loads(resp.text)

    # return empty array if there are no results
    if not search_results:
        return []

    for result in search_results:
        # append result
        results.append({'url': result['page_url'],
                        'title': result['title'],
                        'content': '',
                        'img_src': result['url'],
                        'template': 'images.html'})

    # return results
    return results
