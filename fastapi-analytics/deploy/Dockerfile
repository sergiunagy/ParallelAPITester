ARG baseImage=python
ARG baseVersion=3.13.0-bookworm

FROM ${baseImage}:${baseVersion} AS development

ARG baseImage=python
ARG baseVersion=3.13.0-bookworm
LABEL maintainer="sergiu.nagy"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt