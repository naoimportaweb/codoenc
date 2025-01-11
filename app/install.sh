#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root/Por favor, execute como root"
    exit
fi

if [ -L ${DIR} ] ; then
    echo "O diretório ${DIR} nao pode ser usado pois é um link simbólico."
    exit 0
fi

apt update -y
apt install python3-pip -y
apt install libxcb-* -y

# para DEBIAN precisa do --break-system-packages para os outros OSs não
if [ ! -f /etc/pip.conf ] ; then
    touch /etc/pip.conf
    echo '[global]' > /etc/pip.conf
    echo 'break-system-packages = true' >> /etc/pip.conf
fi
pip3 install requests
pip3 install PySide6
pip3 install pycryptodome
pip3 install colorama

chmod +x /opt/codoencrypt/app
chmod +x /opt/codoencrypt/app/gui
chmod +x /opt/codoencrypt/app/gui/view
chmod +r /opt/codoencrypt/app
chmod +r /opt/codoencrypt/app/gui
chmod +r /opt/codoencrypt/app/gui/view
chmod +r /opt/codoencrypt/api
chmod +x /opt/codoencrypt/api
chmod +r /opt/codoencrypt/app/gui/codog
chmod +x /opt/codoencrypt/app/gui/codog
chmod +r /opt/codoencrypt/app/gui/codog.py

ln -s /opt/codoencrypt/app/gui/codog /bin/codog
