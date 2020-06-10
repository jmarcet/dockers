#!/bin/sh

source ./.env
sed -e "s:\${IN_KEY}:${IN_KEY}:" \
    -e "s:\${IN_CER}:${IN_CER}:" \
    -e "s:\${IN_PW}:${IN_PW}:g" \
    -e "s:\${UNIFI_PW}:${UNIFI_PW}:g" \
    ./updatecert.sh >| /tmp/._updatecert.sh
chmod +x /tmp/._updatecert.sh
docker cp /tmp/._updatecert.sh unifi:/usr/lib/unifi/updatecert.sh
docker exec -it unifi /usr/lib/unifi/updatecert.sh
rm -f /tmp/._updatecert.sh
