FROM python:2.7-slim

ENV HOME="/config"
ENV PATH="/app:/config/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV TERM="screen-256color"
ENV _pkg="rtorrent-ps-ch_1.8.3-0.9.8-debian-buster_amd64.deb"

RUN mkdir -p /app /config/bin /config/.local /config/rtorrent

RUN apt-get -y update && apt-get -y install bash-completion binutils cron curl dialog git \
    iperf3 iproute2 less libcppunit-dev lsb-release lsof msmtp procps tmux s6 vim wget

# build rtorrent-ps-ch deb
# RUN apt-get -y install sudo tmux coreutils binutils build-essential subversion git time \
#     chrpath pkg-config libssl-dev libncurses5-dev libncursesw5-dev locales libcppunit-dev \
#     zlib1g-dev autoconf automake libtool libxml2-dev libxslt1-dev curl ruby ruby-dev mc \
#     python python-dev python-virtualenv python-pip python-setuptools python-pkg-resources
# RUN gem install fpm
#
# WORKDIR /src
# COPY ./dl-fix.patch .
# RUN git clone https://github.com/chros73/rtorrent-ps-ch.git \
#     && cd rtorrent-ps-ch \
#     && patch -p1 < ../dl-fix.patch
#
# WORKDIR /src/rtorrent-ps-ch
# RUN time nice -n 19 env optimize_build=no ./build.sh ch
# RUN ./build.sh install
# RUN debfullname="Javier Marcet" debemail="javier@marcet.info" ./build.sh pkg2deb

COPY ./$_pkg /tmp/
RUN dpkg -i /tmp/$_pkg && rm -f /tmp/$_pkg

WORKDIR /config
RUN git clone "https://github.com/pyroscope/pyrocore.git" ~/.local/pyroscope
RUN ~/.local/pyroscope/update-to-head.sh
# RUN ~/.local/pyroscope/src/scripts/make-rtorrent-config.sh

COPY ./start.sh /app/
COPY ./config/.* /config/
RUN rm -fr /etc/crontabs && ln -s /var/spool/cron/crontabs /etc/
COPY --chown=65534 ./crontab /etc/crontabs/nobody

WORKDIR $HOME

CMD /app/start.sh

