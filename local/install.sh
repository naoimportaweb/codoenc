#!/bin/bash

if [ -d /opt/codoencrypt ] ; then
    echo "Diretório já existe: /opt/codoencrypt"
    exit 1
fi

if [ -d /tmp/codoencrypt-main/ ] ; then
    rm -r /tmp/codoencrypt-main/
fi

mkdir /opt/codoencrypt

wget -O /tmp/codoencrypt-main.zip http://www.aied.com.br/linux/download/kfm/codoencrypt-main.zip
unzip /tmp/codoencrypt-main.zip -d /tmp/
cp -r /tmp/codoencrypt-main/* /opt/codoencrypt/

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

