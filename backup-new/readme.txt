Connect to OPI: - Windows (ssh root@10.242.51.23)
		- Linux (sudo ssh 10.242.51.23)
Change directory: cd /var/www
Check Bluetooth connect to device: hcitool con

Manual connect Bluetooth: bluetoothctl
- power on/off (bluetoothctl power on/off)
- Scan bluetooth nearby: scan on
- Connect bluetooth: connect [Address]
- Pair Bluetooth: pair [Address]
- Trust Device: trust [Address]

Check internet: speedtest-cli --simple

Check log bluetooth connect: nano logfile.log
Check log gate : nano logfilepy.log

