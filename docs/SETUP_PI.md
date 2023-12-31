# Setup A New Pi
On a fresh raspberry PI (tested with raspbian bookworm)

## Current PIs
----------------
| Hostname | IP Address    | Notes |
|----------|---------------|-------|
| wx3      | 192.168.99.23 | Unreachable atm |
| wx4      | 192.168.99.24 | Unreachable atm |
| wx5      | 192.168.99.25 | Bastion Node Going up this winter |
| wx6      | 192.168.99.26 | Currently just an SD Card |
| wx7      | 192.168.99.27 | Currently just an SD Card |

- Gateway: 192.168.99.1
- DNS: 192.168.99.1

## PI hostname
sequentially number the PIs (wx3, wx4, wx5, etc)
and add the new one to the table above

```bash

## Users
Create a new user that all admins can su into (called `pi`)
```bash
sudo adduser pi
sudo usermod -aG sudo pi
```

Create a user for each admin for the pi, and give them a temporary password for them to update on first login
```example
sudo adduser john
```


## Install Software

### Clone source code
```bash
sudo apt install git
git clone https://github.com/joram/accvi-5040-hut.git
cd accvi-5040-hut
```

### Create `.env` secrets
```
# used to create dns routes
HOSTNAME=wx5
CLOUDFLARED_TUNNEL_ID=...
FIXED_IP_ADDRESS=192.168.99.25

# used to backup webcam images and weather data to S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=ca-central-1
```

```bash
make setup
make install
```
