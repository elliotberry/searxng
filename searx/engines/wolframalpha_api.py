# Wolfram Alpha (Maths)
#
# @website     http://www.wolframalpha.com
# @provide-api yes (http://api.wolframalpha.com/v2/)
#
# @using-api   yes
# @results     XML
# @stable      yes
# @parse       result

from urllib import urlencode
from lxml import etree
from searx.engines.xpath import extract_text
from searx.utils import html_to_text

# search-url
base_url = 'http://api.wolframalpha.com/v2/query'
search_url = base_url + '?appid={api_key}&{query}&format=plaintext'
site_url = 'http://wolframalpha.com/input/?{query}'

#embedded_url = '<iframe width="540" height="304" ' +\
#    'data-src="//www.youtube-nocookie.com/embed/{videoid}" ' +\
#    'frameborder="0" allowfullscreen></iframe>'

# do search-request
def request(query, params):
    params['url'] = search_url.format(query=urlencode({'input': query}),
                                      api_key=api_key)

    # need this for url in response
    global my_query
    my_query = query

    return params

# replace private user area characters to make text legible
def replace_pua_chars(text):
    pua_chars = { u'\uf74c': 'd',
                  u'\uf74d': u'\u212f',
                  u'\uf74e': 'i',
                  u'\uf7d9': '=' }

    for k, v in pua_chars.iteritems():
        text = text.replace(k, v)

    return text

# get response from search-request
def response(resp):
    results = []

    search_results = etree.XML(resp.content)

    # return empty array if there are no results
    if search_results.xpath('/queryresult[attribute::success="false"]'):
        return []

    # parse result
    result = search_results.xpath('//pod[attribute::primary="true"]/subpod/plaintext')[0].text
    result = replace_pua_chars(result)

    # bind url from site
    result_url = site_url.format(query=urlencode({'i': my_query}))

    # append result
    results.append({'url': result_url,
                    'title': result})

    # return results
    return results
