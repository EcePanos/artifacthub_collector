import os
import requests
import json
from datetime import datetime

ARTIFACTHUB_BASE_URL = "https://artifacthub.io/api/v1"
ARTIFACTHUB_REPO_SEARCH_URL = "repositories/search"
ARTIFACTHUB_PKG_SEARCH_URL = "packages/search"

# API request common headers
common_headers = {
    'accept': 'application/json'
}

def _api_search_repo(offset=0, limit=60):

    # we need authorization for the repos endpoint

    # try to read API key information form environment
    # export vars or replace the None with a valid API for local testing
    API_KEY_ID = os.getenv('ARTIFACT_HUB_API_KEY_ID', None)
    if API_KEY_ID is None:
        raise ValueError("Artifact Hub API key ID is missing")
    API_KEY_SECRET = os.getenv('ARTIFACT_HUB_API_KEY_SECRET', None)
    if API_KEY_SECRET is None:
        raise ValueError("Artifact Hub API key Secret is missing")

    # merge common headers with auth
    _headers = {
        **common_headers,
        'X-API-KEY-ID': API_KEY_ID,
        'X-API-KEY-SECRET': API_KEY_SECRET
        }

    params = {
        'offset': str(offset),
        'limit': str(limit)
    }
    return requests.get(f'{ARTIFACTHUB_BASE_URL}/{ARTIFACTHUB_REPO_SEARCH_URL}', headers=_headers, params=params).json()

def _api_search_packages(offset=0, limit=60):
    params = {
        'offset': str(offset),
        'limit': str(limit)
    }
    result = requests.get(f'{ARTIFACTHUB_BASE_URL}/{ARTIFACTHUB_PKG_SEARCH_URL}', headers=common_headers, params=params).json()
    return result['packages']

def _api_iterate_paged(api_wrapper, slice_size=60):
    _result = []

    _limit = slice_size
    _offset = 0

    _response = api_wrapper(offset=_offset, limit=_limit)

    while len(_response) != 0:
        # extent resultset
        _result.extend(_response)
        # extent offset to next slice
        _offset += _limit
        # call ArtifactHUB API
        _response = api_wrapper(offset=_offset, limit=_limit)
        print(len(_result))

    return _result

def get_repositories():
    """
    Collects all repositories from ArtifactHUB using the /respoitories/search API.
    https://artifacthub.io/docs/api/#/Repositories/searchRepositories
    It requires a valid API key to function as this API endpoint needs authentication.
    """

    print("Retrieving repositories ...")
    repos = _api_iterate_paged(_api_search_repo, slice_size=60)

    print("Writing output dataset ...")
    with open(f'data/repos-{datetime.date(datetime.now())}.json', 'w') as f:
        json.dump(repos, f, indent=4)

def get_packages():
    """
    Collects metadata of all packages from ArtifactHUB using the /packages/search API.
    https://artifacthub.io/docs/api/#/Packages/searchPackages
    """

    print("Retrieving packages ...")
    packages = _api_iterate_paged(_api_search_packages, slice_size=60)

    print("Writing output dataset ...")
    with open(f'data/packages-{datetime.date(datetime.now())}.json', 'w') as f:
        json.dump(packages, f, indent=4)
