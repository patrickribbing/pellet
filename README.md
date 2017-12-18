# pellet
This is a Raspberry Pi Zero W project that use a HC-SR04 distance sensor to measure the amount of pellets in a silo. 

A python script is started at system startup and then reads the distance every 10 seconds. The value is written to a text file located in the web directory. A web page can access the file, or the file may be read by a script running in Domoticz. 

## Installation
Edit the python script to set pins for the distance sensor. Also set the path and name of the file to write the distance value to.

Install Raspbian on Raspberry Pi Zero W. In this setup the hardware will live in a box close to the pellets burner, hence there is no need for a graphical gui. Configure the WLAN (may be tricky, Google is your friend, many tutorials miss that the WPA supplicant country is needed).

Copy the python script to a suitable location. 

Copy the startup script to `/etc/init.d/pellets`. Make the script executable with `chmod +x pellets`. Make the script startable with `update-rc.d pellets defaults`. Reboot and verify the script has started.

A web server is needed if someone else shall be able to read the distance file (well, other solutions are of course possible, such as FTP access). One server with a small footprint is NGINX. Install it and make sure the web directory and the file path in the python script match.
