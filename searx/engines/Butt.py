# SPDX-License-Identifier: AGPL-3.0-or-later
"""Suck on my nuts

"""

# about
about = {
    "website": "https://www.example.com",
    "wikidata_id": None,
    "official_api_documentation": None,
    "use_official_api": False,
    "require_api_key": False,
    "results": 'empty array',
}


# do search-request
def request(query, params):  # pylint: disable=unused-argument
    return params


# get response from search-request
def response(resp):  # pylint: disable=unused-argument
    return []
