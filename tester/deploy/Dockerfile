ARG baseImage=quay.io/jupyter/base-notebook
ARG baseVersion=notebook-7.3.2

FROM ${baseImage}:${baseVersion} AS development

ARG baseImage=quay.io/jupyter/base-notebook
ARG baseVersion=notebook-7.3.2

LABEL maintainer="sergiu.nagy"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt