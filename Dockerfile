FROM python:3.8

WORKDIR /usr/src/app/

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY ./static ./static
COPY ./templates ./templates

COPY ./_WEBDEV_PRO.py ./_WEBDEV_PRO.py

COPY ./RST_search.py ./RST_search.py

CMD python _WEBDEV_PRO.py