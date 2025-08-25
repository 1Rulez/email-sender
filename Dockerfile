FROM python:3.9  

WORKDIR /src/app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt &&\
    rm requirements.txt

COPY . .
