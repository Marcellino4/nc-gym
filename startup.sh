#!/bin/bash

# Start VNC server
gnome-terminal -- bash -c "vncserver :1 -geometry 1024x768 -depth 24; exec bash"
sleep 30

# Connect to the first Bluetooth device
gnome-terminal -- bash -c "
bluetoothctl << EOF
connect DC:0D:30:93:BF:11
EOF

# Loop until the device is connected
until bluetoothctl info DC:0D:30:93:BF:11 | grep -q 'Connected: yes'; do
    sleep 5
    bluetoothctl connect DC:0D:30:93:BF:11
done
exec bash"
sleep 30

# Connect to the second Bluetooth device
gnome-terminal -- bash -c "
bluetoothctl << EOF
connect DC:0D:30:93:BF:8C
EOF

# Loop until the device is connected
until bluetoothctl info DC:0D:30:93:BF:8C | grep -q 'Connected: yes'; do
    sleep 5
    bluetoothctl connect DC:0D:30:93:BF:8C
done
exec bash"
sleep 30

# Connect rfcomm0
gnome-terminal -- bash -c "sudo rfcomm connect rfcomm0 98:D3:31:FB:5E:5C; exec bash"
sleep 30

# Connect rfcomm1
gnome-terminal -- bash -c "sudo rfcomm connect rfcomm1 98:D3:31:FB:5F:57; exec bash"
sleep 30

# Run the first Python script
gnome-terminal -- bash -c "cd /var/www/nc-gym && python test.py; exec bash"
sleep 30

# Run the second Python script
gnome-terminal -- bash -c "cd /var/www/nc-gym && python test2.py; exec bash"