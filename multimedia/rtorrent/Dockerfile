FROM alpine

RUN apk add bash iproute2 iputils procps rtorrent s6

ENV HOME="/config"

WORKDIR /app

COPY ./start.sh .

CMD /app/start.sh

