
all: build

build:
	docker compose up --build -d client server
	@echo "Waiting for containers to initialize..."

	# wait for the client container to be ready its the heaviest one
	@while ! docker inspect client >/dev/null 2>&1; do sleep 1; done
	@echo CLIENTIP=$$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' client) > .env
	@echo CLIENTMAC=$$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' client) >> .env
	@echo SERVERIP=$$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server) >> .env
	@echo SERVERMAC=$$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' server) >> .env

	@echo "Client IP: $$(grep CLIENTIP .env | cut -d '=' -f2)"
	@echo "Client MAC: $$(grep CLIENTMAC .env | cut -d '=' -f2)"
	@echo "Server IP: $$(grep SERVERIP .env | cut -d '=' -f2)"
	@echo "Server MAC: $$(grep SERVERMAC .env | cut -d '=' -f2)"

	# Pass variables to arp_spoofer
	docker compose --env-file .env up --build -d arp_spoofer

re:
	docker compose down
	$(MAKE) build

spoofer:
	@echo 'python3 inquisitor.py $$CLIENTIP $$CLIENTMAC $$SERVERIP $$SERVERMAC' | xclip -selection c
	@echo "Command copied to clipboard. Paste it inside the arp_spoofer container."
	docker exec -it arp_spoofer /bin/bash

arp_tables:
	docker exec -it client /bin/bash -c "ip neigh"