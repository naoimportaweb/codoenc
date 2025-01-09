#!/bin/bash

DIR=/opt/codoencrypt/

if [ "$EUID" -ne 0 ]
  then echo "Please run as root/Por favor, execute como root"
  exit 0
fi

if [ -L ${DIR} ] ; then
    echo "O diretório ${DIR} nao pode ser usado pois é um link simbólico."
    exit 0
fi

if [ -d ${DIR} ] ; then
    mkdir ${DIR}
fi

cp -r ../* ${DIR}
chmod +x ${DIR}local/start.sh

sudo apt install cryptsetup -y

echo "[Unit]" > /etc/systemd/system/kfm_codo.service
echo "Description=Codoencrypt local" >> /etc/systemd/system/kfm_codo.service
echo "[Service]" >> /etc/systemd/system/kfm_codo.service
echo "Type=forking" >> /etc/systemd/system/kfm_codo.service
echo "Environment=SUDO_USER=$SUDO_USER" >> /etc/systemd/system/kfm_codo.service
echo "ExecStart=/bin/bash ${DIR}/local/start.sh &" >> /etc/systemd/system/kfm_codo.service
echo "[Install]" >> /etc/systemd/system/kfm_codo.service
echo "WantedBy=graphical.target" >> /etc/systemd/system/kfm_codo.service

systemctl daemon-reload
systemctl enable kfm_codo.service
systemctl start kfm_codo.service

