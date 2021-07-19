import json
import glob
import subprocess
from pathlib import Path


def download_helm():
    """
    Parses scraped packages JSON and downloads all helm charts that were found
    """


    filenames = glob.glob("data/packages-*.json")
    filenames.sort()
    with open(filenames[-1]) as input:
        data = json.load(input)
    count = 0
    charts = {}
    for package in data:
        if package['repository']['kind'] == 0:
            repo_name = package['repository']['name']
            repo_url = package['repository']['url']
            chart_name = package['normalized_name']
            version = package['version']
            count += 1
            charts[chart_name] = {
                'repo_name': repo_name,
                'repo_url': repo_url,
                'chart_name': chart_name,
                'version': version
            }
    
    count = 0

    # make sure download target directory exists
    _download_target_dir = 'data/charts'
    Path(_download_target_dir).mkdir(parents=True, exist_ok=True)

    # add helm repo and download chart
    for item in charts:
        print(f'Pulling chart {count + 1} of {len(charts)}')

        subprocess.run(f"helm repo add {charts[item]['repo_name']} {charts[item]['repo_url']}", shell=True)
        #subprocess.run(f"helm pull {charts[item]['repo_name']}/{charts[item]['chart_name']} --version {charts[item]['version']} -d {_download_target_dir}", shell=True)
        subprocess.run(f"helm pull {charts[item]['repo_name']}/{charts[item]['chart_name']} --version {charts[item]['version']} -d {_download_target_dir} --untar --untardir {charts[item]['repo_name']}/{charts[item]['chart_name']}-{charts[item]['version']}", shell=True)
        count += 1
