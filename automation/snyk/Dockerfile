FROM ${OPENVINO_UBUNTU_IMAGE}

ARG http_proxy
ARG https_proxy
ARG no_proxy
ARG docker_username

ENV USER_NAME ${docker_username}
ENV http_proxy ${http_proxy}
ENV https_proxy ${https_proxy}
ENV no_proxy ${no_proxy}
ENV PYTHON_VERSION 3.6
ENV PYTHON python${PYTHON_VERSION}

USER root

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -

RUN apt-get update && \
    apt install -y --no-install-recommends apt-utils \
    nodejs \
    jq \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-pip \
    python3-setuptools \
    python${PYTHON_VERSION}-dev

RUN ${PYTHON} -m pip install pip

COPY --from=snyk/snyk:linux /usr/local/bin/snyk /usr/local/bin/snyk

RUN npm install snyk-to-html -g

COPY ./docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
