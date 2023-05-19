#server.dockerfile

FROM python:3.10.10-bullseye
LABEL name="hail"
LABEL version="1.5"

WORKDIR /app
COPY ../ /app
RUN  pip install --upgrade pip==22.0.4 \
     && pip install -r requirements.txt \

ENV CLIENT_PORT=88 \
    CLIENT_HOST=000.0.0.0 \
    model=fedavg \
    k_clients=4 \
    n_epochs=10

CMD python client/run_server.py --CLIENT_PORT ${CLIENT_PORT} --CLIENT_HOST ${CLIENT_HOST} --model ${model}





