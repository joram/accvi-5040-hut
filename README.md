# ACCVI Hišimy̓awiƛ Hut
This repository is for managing the software for the weather station and camera, controlled from a raspberryPi in [the ACCVI Hut on 5040 Peak](https://accvi.ca/5040-peak-hut/).

## Setup
On a fresh raspberry PI (tested with raspbian bookworm), check this repo out, and follow along with the Makefile.

TODO: Better documentation of setup process.

## SSH Access

### Install Cloudflared Daemon
to access the servers you need to install the `cloudflared` daemon.
[docs here](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

Note: you do not need a cloudflare account, or to log in to the daemon.

### Add SSH Config
Add the following to your `~/.ssh/config` file:
```
Host ssh-5040.oram.ca
ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h
```

### SSH to Server
The command `ssh <username>@ssh-5040.oram.ca` should now work.






## Weather Station

### S3 5040.oram.ca

### victoriaweather.ca

### wunderground.com
[station here](https://www.wunderground.com/dashboard/pws/IUCLUE4)

## Webcam

### S3 5040.oram.ca

### Windy
once the hut is setup, with a consistent image url for the latest, we can register it here:
https://www.windy.com/-Add-new-webcam/webcams/add?48.477,-123.531,5