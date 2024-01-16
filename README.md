# ACCVI Hišimy̓awiƛ Hut
This repository is for managing the software for the weather station and camera, controlled from a raspberryPi in [the ACCVI Hut on 5040 Peak](https://accvi.ca/5040-peak-hut/).

## System Design/Intent
The system is designed to be as simple as possible, and to be as resilient as possible to power outages and network outages.

All Data from the weather station and camera is cached on the pi, stored in this repository's `./data` directory.
This directory is specially mounted as a ramfs filesystem, so that it is stored in memory, and not on the SD card.
- UPSIDE: the SD card doesn't burn out.
- DOWNSIDE: data is lost on reboot, and is not backed up.
The cron job scripts in their respective directories are responsible for backing up the data, and flushing it from their respective directories.

## System Diagram
```mermaid
classDiagram
class Antenna {
    Physically up a tree behind the hut
}

class BulletModem {
    IP: 192.168.99.1
}

namespace Sensors {

    class IPCamera {
        Model: Speco technologies O2iD8
        IP: 192.168.99.149 ??? 192.168.99.150
        Location: on the top of the front poll
    }
    
    class WeatherStation {
        Model: Davis Vantage Pro 2
        IP: 192.168.99.23
    }
}

namespace Computers {
    class RPI_Wx3 {
        Model: Raspberry Pi
        IP: 192.168.99.23
    }
    
    class RPI_Wx4 {
        Model: Raspberry Pi
        IP: 192.168.99.24
    }
    
    class RPI_Wx5 {
        Model: Raspberry Pi
        IP: 192.168.99.25
    }
}

class WifiRouter {
    IP: 192.68.99.128
}

class PoEInjector1 {
    
}

class PoEInjector2 {
    
}

class Switch {
    model: Netgear switch (blue)
}

Antenna -- BulletModem
BulletModem -- Switch
Switch -- PoEInjector1
PoEInjector1 -- IPCamera : running under the eaves
Switch -- PoEInjector2
PoEInjector2 -- WeatherStation : 250ft cable to antenna
Switch -- RPI_Wx3
Switch -- RPI_Wx4
Switch -- RPI_Wx5
Switch -- WifiRouter
```

## Weather Station
the weather station script (`./weather_station/cron.sh`) is responsible for:
- getting the data
- backing up the data up
- and flushing it from the `./data/weather_station` directory.

### Backup Locations:
#### victoriaweather.ca

#### wunderground.com
[station here](https://www.wunderground.com/dashboard/pws/IUCLUE4)

#### S3 5040.oram.ca

## Webcam
the webcam script (`./webcam/cron.sh`) is responsible for:
- getting the data
- backing up the data up
- and flushing it from the `./data/webcam` directory.

### Backup Locations:
#### Windy
once the hut is setup, with a consistent image url for the latest, we can register it here:
https://www.windy.com/-Add-new-webcam/webcams/add?48.477,-123.531,5
#### S3 5040.oram.ca
