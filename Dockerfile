FROM python:3.11-bookworm

RUN python3 -m pip install aiohttp
RUN apt update && apt install -y ipmitool

WORKDIR /app

COPY server.py /app/

CMD ["python3", "server.py", "--port", "8799"]
