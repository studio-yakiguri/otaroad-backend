#!bin/bash
NEXTCLOUD_CONTAINER_IP="172.21.0.3"
curl -k -X GET https://$NEXTCLOUD_CONTINER_IP/s/CYj5AYns7mF2soC/download --output secure.tar
tar -xvf secure.tar
mv .secure /subculture-map-backend