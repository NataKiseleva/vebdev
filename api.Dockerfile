FROM python:3.8

ARG ROOT_PATH
ENV ROOT_PATH=$ROOT_PATH

WORKDIR /usr/src/app/

COPY ./api/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY ./data ./data
COPY ./api ./api
COPY ./RST_search.py ./RST_search.py
