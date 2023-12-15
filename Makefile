include .env
$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))


install: setup
	cloudflared login

	# creates a tunnel for the pi, and all appropriate dns entries.
	#cloudflared tunnel create hut_pi_${HOSTNAME}
	cloudflared tunnel route dns hut_pi_${HOSTNAME} 5040-${HOSTNAME}.oram.ca
	cloudflared tunnel route dns hut_pi_${HOSTNAME} ssh-5040-${HOSTNAME}.oram.ca
	cloudflared tunnel route dns hut_pi_${HOSTNAME} hello-world-5040-${HOSTNAME}.oram.ca

	# remove previous
	sudo cloudflared service uninstall
	sudo rm /etc/cloudflared/config.yml

	# creates a systemd service for the tunnel
	rm ${HOSTNAME}-cloudflared.yaml
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

_setup_ramfs:
	sudo chmod 777 /etc/fstab
	sudo echo "tmpfs /var/log tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0" >> /etc/fstab
	sudo echo "tmpfs /home/pi/accvi-5040-hut/data tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0" >> /etc/fstab
	sudo sort -u /etc/fstab  # remove duplicate lines
	sudo systemctl daemon-reload
	sudo mount -a

setup_wifi:
	cat ./setup_files/hut_wifi.template.nmconnection | envsubst > hut_wifi.nmconnection
	cp ./hut_wifi.nmconnection /etc/NetworkManager/system-connections/hut_wifi.nmconnection
	sudo chmod 700 /etc/NetworkManager/system-connections/hut_wifi.nmconnection
	sudo chown root:root /etc/NetworkManager/system-connections/hut_wifi.nmconnection
	nmcli reload ${WIFI_SSID}
