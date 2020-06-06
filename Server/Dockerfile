FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir  -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]

ARG MODE

CMD [ "run.py ${MODE}" ]
