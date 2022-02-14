############## build stage ##############
FROM python:3.10-alpine AS buildstage

ARG LIBTORRENT_VER=0.13.8
ARG RTORRENT_VER=0.9.8
ARG VER=1.8.4

COPY libtorrent-patches/ /tmp/libtorrent-patches/
COPY rtorrent-patches/ /tmp/rtorrent-patches/

RUN sed -e 's:alpine\/[.0-9v]\+\/:alpine/edge/:g' -i /etc/apk/repositories
RUN apk update && apk upgrade --available --prune --purge
RUN apk add autoconf automake build-base c-ares-dev curl-dev git libtool \
    linux-headers ncurses-dev openssl-dev xmlrpc-c-dev zlib-dev

RUN \
    cd /tmp && \
    wget https://github.com/rakshasa/libtorrent/archive/v${LIBTORRENT_VER}.tar.gz && \
    tar xzf v${LIBTORRENT_VER}.tar.gz && \
    cd libtorrent-${LIBTORRENT_VER} && \
    patch -p1 < /tmp/libtorrent-patches/lt-ps_all_02-better-bencode-errors_all.patch && \
    patch -p1 < /tmp/libtorrent-patches/backport_lt_all_01-partially_done_and_choke_group_fix.patch && \
    patch -p1 < /tmp/libtorrent-patches/backport_lt_all_02-honor_system_file_allocate_fix.patch && \
    ./autogen.sh && \
    ./configure --prefix=/usr --disable-debug && \
    make -j4 && \
    make DESTDIR=/tmp/libtorrent-build install && \
    make install

RUN \
    cd /tmp && \
    wget https://github.com/rakshasa/rtorrent/archive/v${RTORRENT_VER}.tar.gz && \
    tar xzf v${RTORRENT_VER}.tar.gz && \
    cd rtorrent-${RTORRENT_VER} && \
    rt_hex_version=$(printf "0x%02X%02X%02X" ${VER//./ }) && \
    sed -i "s:\\(AC_DEFINE(HAVE_CONFIG_H.*\\):\1  AC_DEFINE(RT_HEX_VERSION, $rt_hex_version, for CPP if checks):" configure.ac && \
    sed -i "s%rTorrent \\\" VERSION \\\"/\\\"%rtorrent-ps-ch $VER \\\"%" src/ui/download_list.cc && \
    sed -i "s%std::string(torrent::version()) + \\\" - \\\" +%%" src/ui/download_list.cc && \
    cp /tmp/rtorrent-patches/*.cc /tmp/rtorrent-patches/*.h src/ && \
    (for patch in /tmp/rtorrent-patches/*.patch; do patch -p1 < $patch; done) && \
    ./autogen.sh && \
    ./configure --prefix=/usr --disable-debug --with-ncursesw --with-xmlrpc-c && \
    make -j4 && \
    make DESTDIR=/tmp/rtorrent-build install


############## runtime stage ##############
FROM python:3.10-alpine

ENV HOME="/config"
ENV PATH="/app:/config/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV TERM="screen-256color"

RUN sed -e 's:alpine\/[.0-9v]\+\/:alpine/edge/:g' -i /etc/apk/repositories
RUN apk update && apk upgrade --available --prune --purge
RUN apk add bash c-ares curl git htop ncurses openssl s6 tmux vim xmlrpc-c-dev zlib

COPY --from=buildstage /tmp/libtorrent-build/usr/lib/ /usr/lib/
COPY --from=buildstage /tmp/rtorrent-build/usr/ /usr/

COPY ./rtorrent.sh /usr/local/bin/
COPY ./config/.* /config/

CMD /usr/local/bin/rtorrent.sh
