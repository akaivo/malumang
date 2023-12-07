#!/bin/bash

echo "# Disable bluetooth by default" >> /boot/config.txt
echo "dtoverlay=disable-bt" >> /boot/config.txt

systemctl disable hciuart.service
systemctl disable bluealsa.service
systemctl disable bluetooth.service
