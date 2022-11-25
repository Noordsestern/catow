FROM python:3-alpine 

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

ENV CAMUNDA_TOPIC ""
ENV POLLING_INTERVAL 3
ENV CAMUNDA_URL http://localhost:8080
ENV DESTINATION_URL "https://github.com/Noordsestern/catow"
ENV PORT 5003

ADD . .
RUN pip install .

EXPOSE ${PORT}

ENTRYPOINT exec python3 -m Catow.main -t ${CAMUNDA_TOPIC} -r ${DESTINATION_URL} -p ${PORT} -i ${POLLING_INTERVAL} -c ${CAMUNDA_URL}
