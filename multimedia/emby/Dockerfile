FROM ghcr.io/linuxserver/emby
COPY ffmpeg.sh /usr/bin
RUN ln -s /app/emby/EmbyServer /usr/bin/EmbyServer && \
    sed -e 's:\/app\/emby\/::g' -e 's:ffmpeg ffmpeg :ffmpeg ffmpeg.sh :' -i /etc/services.d/emby/run

RUN apt-get update && apt-get -y install i965-va-driver ffmpeg
RUN apt-get -y clean && apt-get -y autoremove
