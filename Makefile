include .env

install: setup
	# creates a tunnel for the pi, and all appropriate dns entries.
	cloudflared tunnel create hut_pi_$HOSTNAME
	cloudflared tunnel route dns hut_pi_$HOSTNAME 5040-$HOSTNAME.oram.ca
	cloudflared tunnel route dns hut_pi_$HOSTNAME ssh-5040-$HOSTNAME.oram.ca
	cloudflared tunnel route dns hut_pi_$HOSTNAME hello-world-5040-$HOSTNAME.oram.ca

	# creates a systemd service for the tunnel
	cat ./setup_files/cloudflared.template.yaml | envsubst > ${HOSTNAME}-cloudflared.yaml
	sudo cloudflared --config ${HOSTNAME}-cloudflared.yaml service install
	sudo systemctl enable cloudflared
	sudo systemctl start cloudflared

	# setup cron jobs
	sudo crontab -u pi /etc/cron.d/cronjobs

setup: _setup_ramfs
	sudo apt install -y curl lsb-release
	curl -L https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-archive-keyring.gpg >/dev/null
	echo "deb [signed-by=/usr/share/keyrings/cloudflare-archive-keyring.gpg] https://pkg.cloudflare.com/cloudflared bookworm main" | sudo tee  /etc/apt/sources.list.d/cloudflared.list
	sudo apt update
	sudo apt install -y cloudflared
	sudo sysctl -w net.core.rmem_max=2500000
	sudo sysctl -w net.core.wmem_max=2500000
	sudo pip install PyVantagePro

_setup_ramfs:
	echo "tmpfs /var/log tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0" >> /etc/fstab
	echo "tmpfs /home/pi/5040_hut_station/data tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0" >> /etc/fstab
	sort -u /etc/fstab  # remove duplicate lines
	mount -a


