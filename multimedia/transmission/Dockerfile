FROM linuxserver/transmission
RUN ln -s transmission-daemon /usr/bin/transmission && \
    sed -e 's:s6-setuidgid:nice -n 19 ionice -c 3 s6-setuidgid:' \
        -e 's:/usr/bin/transmission-daemon:transmission:' \
	-i /etc/services.d/transmission/run
