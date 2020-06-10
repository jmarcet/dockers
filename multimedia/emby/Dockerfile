FROM emby/embyserver:latest
RUN ln -s /system/EmbyServer /usr/bin/EmbyServer && \
    sed -e 's:system/EmbyServer:EmbyServer:' -e 's:/bin/ffdetect:ffdetect:' \
        -e 's:/bin/ffmpeg:ffmpeg:' -e 's:/bin/ffprobe:ffprobe:' \
	-i /etc/services.d/emby-server/run
