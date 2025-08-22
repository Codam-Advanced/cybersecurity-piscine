FROM python:3

WORKDIR /app

RUN apt-get update && apt-get install -y libpcap-dev &&  apt-get install -y net-tools

RUN python3 -m pip install --upgrade scapy

COPY ./inquisitor.py /app

CMD [ "bash", "-c", "python3 -u ./inquisitor.py $CLIENTIP $CLIENTMAC $SERVERIP $SERVERMAC" ]