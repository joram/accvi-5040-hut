install_service:
	echo "Installing service"
	sudo cp internal_dashboard.service /etc/systemd/system/accvi_internal_dashboard.service
	sudo systemctl daemon-reload
	sudo systemctl enable accvi_internal_dashboard.service
	sudo systemctl start accvi_internal_dashboard.service
