FROM bitnami/minideb:latest

MAINTAINER Javier Marcet <javier@marcet.info>

RUN install_packages bird iputils-ping iproute2 macchanger net-tools procps tcpdump unzip vim wget
ADD bird.conf /etc/bird/
ADD server.sh /opt/
ADD start.sh /opt/
ADD settings.xml /home/MovistarTV.Server/

RUN wget --no-check-certificate -O /opt/movistartv.zip https://downloads.sourceforge.net/project/movistartv/Leia/Servidor_independiente/MovistarTV.Server.linux/MovistarTV.Server.linux-2.0.23.zip
RUN unzip /opt/movistartv.zip -d /opt && rm -f /opt/movistartv.zip
RUN ln -s Kodi_MovistarTV_Server.pvr /opt/MovistarTV.Server/Kodi-MovistarTV
RUN chown -R 65534:65534 /home /opt

WORKDIR /opt/MovistarTV.Server/

EXPOSE 5000

ENTRYPOINT ["/opt/start.sh"]
