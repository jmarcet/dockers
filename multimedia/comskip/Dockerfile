FROM python:3.9-slim as buildstage
############## build stage ##############

# package versions
ARG ARGTABLE_VER="2.13"
ARG ARGTABLE_VER1="2-13"

# environment settings
ARG TZ="Europe/Madrid"

# copy patches
COPY patches/ /tmp/patches/

RUN apt-get update && apt-get install -y build-essential autoconf curl git libtool pkg-config \
	libavutil-dev libavformat-dev libavcodec-dev
RUN \
 mkdir -p \
	/tmp/argtable && \
 curl -o \
 /tmp/argtable-src.tar.gz -L \
	"https://sourceforge.net/projects/argtable/files/argtable/argtable-${ARGTABLE_VER}/argtable${ARGTABLE_VER1}.tar.gz" && \
 tar xf \
 /tmp/argtable-src.tar.gz -C \
	/tmp/argtable --strip-components=1 && \
 cp /tmp/patches/config.* /tmp/argtable && \
 cd /tmp/argtable && \
 ./configure \
	--prefix=/usr && \
 make -j 2 && \
 make check && \
 make DESTDIR=/tmp/argtable-build install && \
 cp -pr /tmp/argtable-build/usr/* /usr/

RUN \
 git clone git://github.com/erikkaashoek/Comskip /tmp/comskip && \
 cd /tmp/comskip && \
 ./autogen.sh && \
 ./configure \
	--bindir=/usr/bin \
	--sysconfdir=/config/comskip && \
 make -j 2 && \
 make DESTDIR=/tmp/comskip-build install


############## runtime stage ##############
FROM python:3.9-slim

RUN apt-get update && apt-get upgrade -y && \
	apt-get install -y \
	ffmpeg git htop inotify-tools iputils-ping netcat \
	net-tools mkvtoolnix procps vainfo vim wget

RUN apt-get -y clean && apt-get -y autoremove

# copy local files and buildstage artifacts
COPY --from=buildstage /tmp/argtable-build/usr/ /usr/
COPY --from=buildstage /tmp/comskip-build/usr/ /usr/
COPY comskip.ini /etc/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

COPY comskip-recordings.py .
COPY cleanuprecordings.sh .
COPY start.sh .

USER nobody

#ENTRYPOINT ["/app/start.sh"]
ENTRYPOINT tail -f /dev/null
