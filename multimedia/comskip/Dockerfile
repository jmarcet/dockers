FROM lsiobase/alpine:edge as buildstage
############## build stage ##############

# package versions
ARG ARGTABLE_VER="2.13"

# environment settings
ARG TZ="Europe/Madrid"

# copy patches
COPY patches/ /tmp/patches/

RUN \
 echo "**** install build packages ****" && \
 apk -u add --no-cache \
	build-base \
	autoconf \
	automake \
	curl \
	ffmpeg-dev \
	git \
	libtool \
	pkgconf

RUN \
 echo "**** compile argtable2 ****" && \
 ARGTABLE_VER1="${ARGTABLE_VER//./-}" && \
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
 echo "**** copy to /usr for comskip dependency ****" && \
 cp -pr /tmp/argtable-build/usr/* /usr/

RUN \
 echo "***** compile comskip ****" && \
 git clone git://github.com/erikkaashoek/Comskip /tmp/comskip && \
 cd /tmp/comskip && \
 ./autogen.sh && \
 ./configure \
	--bindir=/usr/bin \
	--sysconfdir=/config/comskip && \
 make -j 2 && \
 make DESTDIR=/tmp/comskip-build install

############## runtime stage ##############
FROM python:alpine

RUN \
 echo "**** install runtime packages ****" && \
 apk add --no-cache \
	ffmpeg \
	inotify-tools \
	mkvtoolnix && \
 rm -rf /var/cache/apk/*

# copy local files and buildstage artifacts
COPY --from=buildstage /tmp/argtable-build/usr/ /usr/
COPY --from=buildstage /tmp/comskip-build/usr/ /usr/
COPY comskip.ini /etc/
COPY comskip-recordings.py /usr/bin/

USER nobody

ENTRYPOINT ["/usr/bin/comskip-recordings.py"]
