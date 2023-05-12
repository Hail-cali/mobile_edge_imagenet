#server.dockerfile

FROM python:3.10.10-bullseye
LABEL name="hail"
LABEL version="1.5"

COPY ../ /app
RUN pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT ["python", "run_server.py"]
CMD ["--SERVER_PORT", "88", "--SERVER_HOST" ,"000.0.0.0", "--model", "fedavg", "--k_clients", "1"]

