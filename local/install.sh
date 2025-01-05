#!/bin/bash

if [ ! -d /opt/codoencrypt ] ; then
    mkdir /opt/codoencrypt
fi

cp -r ../* /opt/codoencrypt/

echo "[Unit]" > /etc/systemd/system/kfm_codo.service
echo "Description=Codoencrypt local" >> /etc/systemd/system/kfm_codo.service
echo "[Service]" >> /etc/systemd/system/kfm_codo.service
echo "Type=forking" >> /etc/systemd/system/kfm_codo.service
echo "Environment=SUDO_USER=$SUDO_USER" >> /etc/systemd/system/kfm_codo.service
echo "ExecStart=/opt/codoencrypt/local/start.sh" >> /etc/systemd/system/kfm_codo.service
echo "[Install]" >> /etc/systemd/system/kfm_codo.service
echo "WantedBy=graphical.target" >> /etc/systemd/system/kfm_codo.service

systemctl daemon-reload
systemctl enable kfm_codo.service
systemctl start kfm_codo.service

