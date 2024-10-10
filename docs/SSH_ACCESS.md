# SSH Access
Each admin should be able to ssh into the pi, then su to the `pi` user, where everything is setup. 
This way each admin has their login, but all the software is running on a centralized account we all have access to.

## Install Cloudflared Daemon
to access the servers you need to install the `cloudflared` daemon.
[docs here](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

Note: you do not need a cloudflare account, or to log in to the daemon.

## Add SSH Config
Add the following to your `~/.ssh/config` file:
```
Host ssh-5040-wx5.oram.ca
ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h

Host ssh-5040-wx6.oram.ca
ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h

Host ssh-5040-wx7.oram.ca
ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h
```

## SSH to Server
The command `ssh <username>@ssh-5040-wx<N>.oram.ca` should now work.

i.e. `ssh john@ssh-5040-wx5.oram.ca`