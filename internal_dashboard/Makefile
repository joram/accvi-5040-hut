install_service:
	echo "Installing service"
	sudo cp accvi_internal_dashboard.service /etc/systemd/system/accvi_internal_dashboard.service
	sudo systemctl daemon-reload
	sudo systemctl enable accvi_internal_dashboard.service
	sudo systemctl start accvi_internal_dashboard.service

install_dependencies:
	echo "Installing dependencies"
	sudo apt install python3-uvicorn python3-fastapi python3-requests

build:
	cd app && npm install
	cd app && npm run build
