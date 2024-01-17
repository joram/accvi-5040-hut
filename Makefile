include .env 
$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env)) 
 
 
install: setup_cloudflared setup_network setup_ssh setup_ramfs 
 
setup_cloudflared:
	# NOTE: do not run this command while using the DNS to ssh in. (without screen)
	sudo apt install -y curl lsb-release
	curl -L https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-archive-keyring.gpg >/dev/null
	echo "deb [signed-by=/usr/share/keyrings/cloudflare-archive-keyring.gpg] https://pkg.cloudflare.com/cloudflared bookworm main" | sudo tee  /etc/apt/sources.list.d/cloudflared.list
	sudo apt update
	sudo apt install -y cloudflared
	sudo sysctl -w net.core.rmem_max=2500000
	sudo sysctl -w net.core.wmem_max=2500000

	cloudflared login

	# creates a tunnel for the pi, and all appropriate dns entries.
	cloudflared tunnel create hut_pi_${HOSTNAME} || true
	cloudflared tunnel route dns hut_pi_${HOSTNAME} 5040-${HOSTNAME}.oram.ca
	cloudflared tunnel route dns hut_pi_${HOSTNAME} ssh-5040-${HOSTNAME}.oram.ca
	cloudflared tunnel route dns hut_pi_${HOSTNAME} hello-world-5040-${HOSTNAME}.oram.ca

	# remove previous
	sudo cloudflared service uninstall || true
	sudo rm /etc/cloudflared/config.yml || true

	# creates a systemd service for the tunnel
	rm ${HOSTNAME}-cloudflared.yaml || true
	cat ./setup_files/cloudflared.template.yaml | envsubst > ${HOSTNAME}-cloudflared.yaml
	sudo cloudflared --config ${HOSTNAME}-cloudflared.yaml service install
	sudo systemctl enable cloudflared
	sudo systemctl start cloudflared
 
setup_network: 
	sudo nmcli c mod "Wired connection 1" ipv4.method manual ipv4.addresses ${FIXED_IP_ADDRESS}/32 ipv4.gateway "192.168.99.1" ipv4.dns "192.168.99.1 8.8.8.8 8.8.4.4"
 
setup_ssh: 
	sudo rm /etc/ssh/sshd_config.d/block_ssh_pi_user || true 
	echo "DenyUsers pi" | sudo tee /etc/ssh/sshd_config.d/block_ssh_pi_user 
 
setup_ramfs: 
	sudo chmod 777 /etc/fstab 
	mkdir -p /home/pi/accvi-5040-hut/data 
	sudo echo "tmpfs /var/log tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0" >> /etc/fstab 
	sudo echo "tmpfs /home/pi/accvi-5040-hut/data tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0" >> /etc/fstab 
	sudo sort -u /etc/fstab  # remove duplicate lines 
	sudo systemctl daemon-reload 
	sudo mount -a
 
setup_cron_jobs: 
	echo "todo"

setup_webcam_cron:
	echo "if this is the first time running this, you will need to run the following command:"
	echo "crontab -e"

	crontab -l > mycron	#write out current crontab
	echo "*/30 * * * * /home/pi/accvi-5040-hut/webcam/cron.sh" >> mycron #echo new cron into cron file
	crontab mycron	#install new cron file
	rm mycron