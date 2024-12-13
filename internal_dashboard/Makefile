install_service:
	echo "Installing service"
	sudo cp accvi_internal_dashboard.service /etc/systemd/system/accvi_internal_dashboard.service
	sudo systemctl daemon-reload
	sudo systemctl enable accvi_internal_dashboard.service
	sudo systemctl start accvi_internal_dashboard.service

install_dependencies:
	echo "Installing dependencies"
	pip install -r requirements.txt