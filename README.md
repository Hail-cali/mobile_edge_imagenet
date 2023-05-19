# Personalized image net based on Mobile-Edge
## `Frame work for fedearte learning on mobile edge`
![frame-work_fed](utils/fed_ac_resized.png?raw=true 'federate_learning')

## frame-work arc
![frame-work](utils/arc.png?raw=true 'frame_work_low')

****
## how to build (Docker)

## Server-docker
```shell
docker build -t hail.pinme.server:1.5 ./server/
```
## Client-docker
```shell
docker build -t hail.pinme.client:1.5 ./client/
```


## How to run

### IMPORTANT !! YOU SHOULD DUMP CONTAINER WITH SECRET
## Server run docker
```shell
docker run -d -e k_clients=5 -e SERVER_PORT=8888 -e SERVER_HOST=111.11.11.1 --name pinme.server hail/pinme.server:1.5
```
## Client Run docker
```shell
docker run -it -e model=fedavg -e n_epochs=10  -e CLIENT_PORT=8888 -e CLIENT_HOST=111.11.11.1 --name pinme.server hail/pinme.client:1.5 
```
## DO NOT COMMIT RUNNING CONTAINER, IT Cause dumped your secret  into docker image layer
- if you want to commit your container and want to be guaranteed, then change port and host when run newly commited image
- 

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