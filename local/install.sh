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

if [ ! -d ${DIR} ] ; then
    mkdir ${DIR}
fi

cp -r ../* ${DIR}
chmod +x ${DIR}local/start.sh
chmod +x ${DIR}app/install.sh
chmod +x ${DIR}app
chmod +x ${DIR}app/gui
chmod +x ${DIR}app/gui/codog

apt update -y
apt install cryptsetup -y
apt install python3-pip -y

pip3 install dropbox
pip3 install mega.py
pip3 install tenacity==8.5.0

echo "[Unit]" > /etc/systemd/system/kfm_codo.service
echo "Description=Codoencrypt" >> /etc/systemd/system/kfm_codo.service
echo "[Service]" >> /etc/systemd/system/kfm_codo.service
echo "Environment=SUDO_USER=$SUDO_USER" >> /etc/systemd/system/kfm_codo.service
echo "ExecStart=python3 ${DIR}local/server.py" >> /etc/systemd/system/kfm_codo.service
echo "[Install]" >> /etc/systemd/system/kfm_codo.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/kfm_codo.service

systemctl daemon-reload
systemctl enable kfm_codo.service
systemctl start kfm_codo.service
