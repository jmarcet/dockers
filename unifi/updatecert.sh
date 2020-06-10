#!/bin/sh

openssl pkcs12 -export -inkey ${IN_KEY} -in ${IN_CER} -out /tmp/cert.p12 -name unifi -password pass:${IN_PW}
keytool -importkeystore -deststorepass ${UNIFI_PW} -destkeypass ${UNIFI_PW} -destkeystore /config/data/keystore -srckeystore /tmp/cert.p12 -srcstoretype PKCS12 -srcstorepass ${IN_PW} -alias unifi -noprompt
pkill -f ace.jar
rm -f /tmp/cert.p12 /usr/lib/unifi/updatecert.sh
