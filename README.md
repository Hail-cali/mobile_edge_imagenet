# Personalized image net based on Mobile-Edge
## `Frame work for fedearte learning on mobile edge`
![frame-work_fed](utils/fed_ac_resized.png?raw=true 'federate_learning')

## frame-work arc
![frame-work](utils/arc.png?raw=true 'frame_work_low')

****

## how to run
> check port forwarding first
> 
> 1. run server :: preset epoch, client_k which you want aggregate some
> 2. run client :: preset epoch same as server, gpu num which you want to put in (if can't, switched to cpu )


- ### Server
- DEV 
- new docker container init
- will be added with new dockerfile
- dockerfile-build
```shell
docker build -t hail/pinme/server:1.5 server/
```
### IMPORTANT !! YOU SHOULD DUMP CONTAINER WITH SECRET  
- dump sectet
```shell
docker commit --change "ENV SERVER_POT=0000"
```

- dockerfile -run
```shell
docker run -d --name pinme.server hail/pinme/server:1.5
```
- shell
```shell
source server/start.sh
```
- python directly
```shell
python run_server.py  --SERVER_PORT 59919 --SERVER_HOST '127.0.0.2' --model fedavg --k_clients 1
```


- ### Client
- new dockerfile 
```shell
docker build -t hail/pinme/client:1.5 client/
```


- dockerfile -run
```shell
docker run -d --name pinme.client1 hail/pinme/client:1.5 
```
- shell
```shell
source clinet/start.sh
```
- python cmd
```shell
python run_client.py --CLIENT_PORT 59919 --CLIENT_HOST '127.0.0.2' --model fedavg --n_epochs 1 --gpu 0
```

- if you want to use server & edge, not locally, then set server's port & host to fit in docker forwarding setting

****
### baseline docker image link
- [@`base docker`](https://github.com/matthewfeickert/Docker-Python3-Ubuntu.git)
### for docker setting guide
- [@`guide`](docker_setting_guide.md)

### base dataset link
- [@`cifar-10`](https://www.cs.toronto.edu/~kriz/cifar.html)

****

## Architecture Description

> -  `communicate` :  communicate stream & copy stream
> -  `models` :  model architecture & federate learning
> -  `worker` :  data & model & network setter, data loader
> -  `fed` :  frame-work hugging phase 
> -  `server` :  server class & run script
> -  `clinet` :  client class & run script
> -  `utils` :  debug, plot, logger



## Citation

<pre><code>
@software{pinME,
  author = {Hail},
  month = {12},
  title = {{Frame-work for federate learning}},
  url = {https://github.com/Hail-cali/pinME},
  version = {1.2.0},
  year = {2021}
}
</code></pre>