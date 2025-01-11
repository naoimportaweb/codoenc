#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root/Por favor, execute como root"
    exit
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

ln -s /opt/codoencrypt/app/gui/codog /bin/codog
