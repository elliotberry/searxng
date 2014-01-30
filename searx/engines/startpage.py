from urllib import urlencode
from lxml import html

base_url = None
search_url = None

# TODO paging
paging = False


def request(query, params):
    global search_url
    query = urlencode({'q': query})[2:]
    params['url'] = search_url
    params['method'] = 'POST'
    params['data'] = {'query': query,
                      'startat': (params['pageno'] - 1) * 10}  # offset
    print params['data']
    return params


def response(resp):
    global base_url
    results = []
    dom = html.fromstring(resp.content)
    # ads xpath //div[@id="results"]/div[@id="sponsored"]//div[@class="result"]
    # not ads: div[@class="result"] are the direct childs of div[@id="results"]
    for result in dom.xpath('//div[@id="results"]/div[@class="result"]'):
        link = result.xpath('.//h3/a')[0]
        url = link.attrib.get('href')
        title = link.text_content()

        content = ''
        if len(result.xpath('./p[@class="desc"]')):
            content = result.xpath('./p[@class="desc"]')[0].text_content()

        results.append({'url': url, 'title': title, 'content': content})

    return results
