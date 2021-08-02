import download
import request
import argparse

cli = argparse.ArgumentParser(description='ArtifactHUB Metadata Collector')

cli.add_argument(
    "process_step",
    choices=['acquire-packages', 'acquire-repos', 'download-helm', 'all'],
    default='acquire-packages',
    nargs='?',
    help='Process step to run. Or use "all" to run all steps intertwined. \'acquire-packages\' is the default action.'
    )

args = cli.parse_args()
if args.process_step == 'acquire-packages':
    # get all packages
    request.get_packages()
elif args.process_step == 'acquire-repos':
    # get all repos - auth required
    request.get_repositories()
elif args.process_step == 'download-helm':
    # download helm charts, needs a local package JSON
    download.download_helm()
elif args.process_step == 'all':
    # run all steps intertwined
    request.get_packages()
    request.get_repositories()
    download.download_helm()
