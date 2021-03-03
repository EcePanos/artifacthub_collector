import json
import glob
import subprocess


def download():
    filenames = glob.glob("data/packages-*.json")
    filenames.sort()
    with open(filenames[-1]) as input:
        data = json.load(input)
    count = 0
    charts = {}
    for item in data:
        for package in item['data']['packages']:
            if package['repository']['kind'] == 0:
                repo_name = package['repository']['name']
                repo_url = package['repository']['url']
                chart_name = package['normalized_name']
                version = package['version']
                count += 1
                charts[chart_name] = {'repo_name': repo_name,
                                      'repo_url': repo_url,
                                      'chart_name': chart_name,
                                      'version': version
                                     }
    count = 0
    for item in charts:
        print(f'Pulling chart {count + 1} of {len(charts)}')

        subprocess.run(f"helm repo add {charts[item]['repo_name']} {charts[item]['repo_url']}", shell=True)
        subprocess.run(f"helm pull {charts[item]['repo_name']}/{charts[item]['chart_name']} --version {charts[item]['version']} -d charts", shell=True)
        count += 1
