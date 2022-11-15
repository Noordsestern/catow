FROM python:3-alpine AS GIT_ALPINE

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

FROM GIT_ALPINE AS CATOW

ENV CAMUNDA_TOPIC ""
ENV POLLING_INTERVAL 3
ENV CAMUNDA_URL http://localhost:8080
ENV DESTINATION_URL "https://github.com/Noordsestern/catow"

ADD . .
RUN pip install .

ENTRYPOINT exec python3 -m Catow.main -t ${CAMUNDA_TOPIC} -r ${DESTINATION_URL} -p 5003 -i ${POLLING_INTERVAL}
