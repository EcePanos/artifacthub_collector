import requests
import json
from datetime import datetime

def get_packages():
    print("Retrieving list of repos...")
    headers = {
        'accept': 'application/json',
        'X-API-KEY': 'your-API-key-here'
    }

    response = requests.get('https://artifacthub.io/api/v1/repositories', headers=headers)
    repos = response.json()
    with open(f'data/repos-{datetime.date(datetime.now())}.json', 'w') as f:
        json.dump(repos, f, indent=4)

    names = []
    print("Retrieving package metadata...")
    for item in repos:
        names.append(item['name'])
    count = 0
    packages = []
    headers = {
    'accept': 'application/json',
    'X-API-KEY': 'your-API-key-here'
    }
    for name in names:
        print(f"Collecting metadata from info {count + 1} of {len(names)}")
        params = (
        ('facets', 'false'),
        ('limit', '50'),
        ('repo', name),
        )

        response = requests.get('https://artifacthub.io/api/v1/packages/search', headers=headers, params=params)
        packages.append(response.json())
        count += 1

    length = 0
    for item in packages:
        length += len(item['data']['packages'])
    print(length)

    with open(f'data/packages-{datetime.date(datetime.now())}.json', 'w') as output:
        json.dump(packages, output, indent=4)
