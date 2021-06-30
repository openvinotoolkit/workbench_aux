FROM ${OPENVINO_UBUNTU_IMAGE}

ARG http_proxy
ARG https_proxy
ARG no_proxy
ARG docker_username

ENV USER_NAME ${docker_username}
ENV http_proxy ${http_proxy}
ENV https_proxy ${https_proxy}
ENV no_proxy ${no_proxy}
ENV PYTHON_VERSION 3.9
ENV PYTHON python${PYTHON_VERSION}

USER root

RUN apt-get update && \
    apt install -y --no-install-recommends apt-utils \
    python3-setuptools \
    python3-pip \
    python${PYTHON_VERSION}-dev

RUN ${PYTHON} -m pip install pip

COPY --from=snyk/snyk:linux /usr/local/bin/snyk /usr/local/bin/snyk

COPY ./docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
