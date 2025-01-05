#!/bin/bash
# ./create_volume.sh
# Criar um volume virtual criptografaod, o usuario nao sabe a senha
# do volume para evitar que ele seja coagido para falar.

createopen(){
	dd if=/dev/urandom of=/tmp/$1.img bs=1M count=$(( $2 * 120  ))
	/usr/sbin/cryptsetup luksFormat /tmp/$1.img <<< 'YES' <<< "$3" <<< "$3"
	echo -n "$3" | /usr/sbin/cryptsetup open --type luks /tmp/$1.img $1
	mkfs.ext4 -L $1 /dev/mapper/$1
	/usr/sbin/cryptsetup close $1
	echo -n "$3" | /usr/sbin/cryptsetup open --type luks /tmp/$1.img $1
	mkdir /tmp/$1
	mount /dev/mapper/$1 /tmp/$1
	echo "Sucesso" > /tmp/$1/status.txt
	chown -R $SUDO_USER:$SUDO_USER "/tmp/$1/"
}
#1 = nome do arquivo/diretorio
#2 = tamanho em GB
#3 = Password do volume
createopen $1 $2 $3

# REFERENCIA:
#https://serverfault.com/questions/513605/how-to-non-interactively-supply-a-passphrase-to-dmcrypt-luksformat
#https://opensource.com/article/21/4/linux-encryption