FROM python:3.13-alpine

RUN apk update

RUN apk add make

WORKDIR app

COPY . .

RUN pip install pipenv

RUN pipenv install

ENTRYPOINT ["make"]

CMD ["start-app"]
