# artifacthub_collector

Metadata collector for the artifacthub repository.

Optional chart downloader included.

## Prerequisites

### ArtifactHUB API Key

Some ArtifactHUB API endpoints require an API key in order to run this tool.

The API key id and secret are expected to be present in the following environment variables:

- `ARTIFACT_HUB_API_KEY_ID`
- `ARTIFACT_HUB_API_KEY_SECRET`

## Execution

The collector offers several tasks that acquire different datasets. Basic CLI parameters can be used to select the desired task to run:

```
python main.py [acquire-packages,acquire-repos,download-helm,all]
```

- **acquire-packages** (default)
    - does not require authentication
    - scrapes all packages from ArtifactHUB along with basic information about their repos
- **acquire-repos**
    - does require authentication
    - scrapes all repositories from ArtifactHUB
- **download-helm**
    - does not require authentication
    - downloads all Helm charts previously scraped by running _acquire-packages_
- **all**
    - does require authentication
    - runs all steps from above in the given order
