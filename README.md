# Personalized image net based on Mobile-Edge
## `Frame work for fedearte learning on mobile edge`

## frame-work arc
![frame-work](utils/arc.png?raw=true 'frame_work_low')

****

## how to run
> check port forwarding first
> 
> 1. run server :: preset epoch, client_k which you want aggregate some
> 2. run client :: preset epoch same as server, gpu num which you want to put in (if can't, switched to cpu )


- ### Server
```shell
source server/start.sh
```
```shell
python run_server.py python  --SERVER_PORT 59919 --SERVER_HOST '127.0.0.2' --model fedavg --k_clients 1
```


- ### Client
```shell
source clinet/start.sh
```
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