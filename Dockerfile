FROM python:3.9.6-slim-buster

WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openssl \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl \
    && curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 \
    && chmod +x get_helm.sh && ./get_helm.sh

RUN mkdir data
RUN mkdir charts

COPY ./request.py ./requirements.txt ./download.py  ./main.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]
