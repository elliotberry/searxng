# SPDX-License-Identifier: AGPL-3.0-or-later
"""
 Google (News)
"""

from urllib.parse import urlencode
from lxml import html
from searx.utils import match_language
from searx.engines.google import _fetch_supported_languages, supported_languages_url  # NOQA # pylint: disable=unused-import

# about
about = {
    "website": 'https://news.google.com',
    "wikidata_id": 'Q12020',
    "official_api_documentation": None,
    "use_official_api": False,
    "require_api_key": False,
    "results": 'HTML',
}

# search-url
categories = ['news']
paging = True
language_support = True
safesearch = True
time_range_support = True
number_of_results = 10

search_url = 'https://www.google.com/search'\
    '?{query}'\
    '&tbm=nws'\
    '&gws_rd=cr'\
    '&{search_options}'
time_range_attr = "qdr:{range}"
time_range_dict = {'day': 'd',
                   'week': 'w',
                   'month': 'm',
                   'year': 'y'}


# do search-request
def request(query, params):

    search_options = {
        'start': (params['pageno'] - 1) * number_of_results
    }

    if params['time_range'] in time_range_dict:
        search_options['tbs'] = time_range_attr.format(range=time_range_dict[params['time_range']])

    if safesearch and params['safesearch']:
        search_options['safe'] = 'on'

    params['url'] = search_url.format(query=urlencode({'q': query}),
                                      search_options=urlencode(search_options))

    if params['language'] != 'all':
        language = match_language(params['language'], supported_languages, language_aliases).split('-')[0]
        if language:
            params['url'] += '&hl=' + language

    return params


# get response from search-request
def response(resp):
    results = []

    dom = html.fromstring(resp.text)

    # parse results
    for result in dom.xpath('//div[@class="g"]|//div[@class="g _cy"]'):
        try:
            r = {
                'url': result.xpath('.//a[@class="l lLrAF"]')[0].attrib.get("href"),
                'title': ''.join(result.xpath('.//a[@class="l lLrAF"]//text()')),
                'content': ''.join(result.xpath('.//div[@class="st"]//text()')),
            }
        except:
            continue

        imgs = result.xpath('.//img/@src')
        if len(imgs) and not imgs[0].startswith('data'):
            r['img_src'] = imgs[0]

        results.append(r)

    # return results
    return results
