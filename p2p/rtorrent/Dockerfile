FROM alpine

RUN apk add bash iperf3 iproute2 iputils procps rtorrent s6 tmux

ENV HOME="/config"

RUN mkdir -p /app /config

WORKDIR /app

COPY ./start.sh .

CMD /app/start.sh

