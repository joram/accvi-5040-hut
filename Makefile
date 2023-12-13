
setup:
	sudo apt install -y curl lsb-release
	curl -L https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-archive-keyring.gpg >/dev/null
	echo "deb [signed-by=/usr/share/keyrings/cloudflare-archive-keyring.gpg] https://pkg.cloudflare.com/cloudflared bookworm main" | sudo tee  /etc/apt/sources.list.d/cloudflared.list
	sudo apt update
	sudo apt install -y cloudflared
	sudo sysctl -w net.core.rmem_max=2500000
	sudo sysctl -w net.core.wmem_max=2500000
	sudo pip install PyVantagePro


create_tunnel:
	cloudflared tunnel login
	echo "note the ID of the tunnel, then run create_tunnel_dns"
	echo "Next, run `make create_tunnel_dns`"

create_tunnel_dns:
	cloudflared tunnel create hut_pi
	cloudflared tunnel route dns hut_pi 5040.oram.ca
	cloudflared tunnel route dns hut_pi ssh-5040.oram.ca
	cloudflared tunnel route dns hut_pi hello-world-5040.oram.ca
	echo "to make sure this starts as a service on boot, run create_cloudflared_service"

run_tunnel:
	cloudflared tunnel --config ./setup_files/cloudflared.yaml run

create_cloudflared_service:
	sudo cloudflared --config ./setup_files/cloudflared.yaml service install
	sudo systemctl enable cloudflared
	sudo systemctl start cloudflared

add_ssh_key:
	ssh-copy-id -i ~/.ssh/id_rsa.pub ssh-5040.oram.ca


martin_install:
	apt install -y raspian-lite mariadb-server proftpd nginx python3-flask libhttp-date-perl
	apt install -y python3-matplotlib
	apt install -y python3-pip
	yes | pip install mysql-connector-python
	yes | pip install -U pymodbus

