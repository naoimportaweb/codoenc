#!/bin/bash

#$1 path
#$2 luksformat 
umount $1
cryptsetup luksClose $2