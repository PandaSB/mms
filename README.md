# mms

Config mms APN free by wvdial : wvdial FREE ( in /etc/wvdial.conf)

[Dialer FREE]
Init1 = ATZ
Init2 = ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0
Init3 = AT+CGDCONT=1,"IP","mmsfree"
Stupid Mode = yes
Modem Type = Analog Modem
Baud = 115200
Modem = /dev/ttyUSB2
Phone = *99#
ISDN = 0
username = "blank"
Password = "blank"

usage : 
sudo wvdial FREE
sudo route del default gw 192.168.0.254 eth0
./mms.py

