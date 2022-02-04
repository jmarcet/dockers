FROM python:3.10-alpine as buildstage
############## build stage ##############

# package versions
ARG ARGTABLE_VER="2.13"
ARG ARGTABLE_VER1="2-13"

# environment settings
ARG TZ="Europe/Madrid"

RUN sed -e 's:alpine\/[.0-9v]\+\/:alpine/edge/:g' -i /etc/apk/repositories
RUN apk update && apk upgrade && apk add autoconf automake build-base curl ffmpeg-dev git libtool
RUN \
    mkdir -p /tmp/argtable && \
    curl -o /tmp/argtable-src.tar.gz -L \
    "https://sourceforge.net/projects/argtable/files/argtable/argtable-${ARGTABLE_VER}/argtable${ARGTABLE_VER1}.tar.gz" && \
    tar xf /tmp/argtable-src.tar.gz -C /tmp/argtable --strip-components=1 && \
    cd /tmp/argtable && \
    ./configure --prefix=/usr && \
    make -j 2 && make check && \
    make DESTDIR=/tmp/argtable-build install && \
    cp -pr /tmp/argtable-build/usr/* /usr/

RUN \
    git clone git://github.com/erikkaashoek/Comskip /tmp/comskip && \
    cd /tmp/comskip && \
    ./autogen.sh && \
    ./configure --bindir=/usr/bin --sysconfdir=/config/comskip && \
    make -j 2 && \
    make DESTDIR=/tmp/comskip-build install

############## runtime stage ##############
FROM python:3.10-alpine

RUN sed -e 's:alpine\/[.0-9v]\+\/:alpine/edge/:g' -i /etc/apk/repositories
RUN apk update && apk upgrade && \
    apk add bash curl ffmpeg git htop inotify-tools libva libva-intel-driver mkvtoolnix s6 sqlite-libs vim && \
    pip install black ipython

# copy local files and buildstage artifacts
COPY --from=buildstage /tmp/argtable-build/usr/lib/ /usr/lib/
COPY --from=buildstage /tmp/comskip-build/usr/ /usr/
COPY comskip.ini /etc/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

COPY comskip-recordings.py .
COPY cleanuprecordings.sh .
COPY start.sh .

ENTRYPOINT ["/app/start.sh"]
