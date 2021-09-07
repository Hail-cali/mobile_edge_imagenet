# docker container

---
## why docker ?

- 파이썬 버전 issue
- 컨테이너 환경을 통해 dependency issue 대응
- 배포 issue


## Setting
- used image : ubuntu 20.04 & python 3.8.9 version 
- 개발 환경 구성에서는 다양한 os 패키지 설치 (sudo, git, ssh 등)
- 배포 시에는 최소한의 요건으로만 구성 예정
- docker는 server와 edge 각각 다른 최적의 이미지로 배포 

### 0)  docker install 
### 1)  image download
<pre><code> docker pull matthewfeickert/docker-python3-ubuntu
</code></pre>
### 2) run image with port forwading
- port forwading 관련 서버에서 포트 설정과 방화벽 설정이 필요
- -p [외부 포트]:[도커 내부 포트]
- 개발환경으로 세팅 시 포트 세개는 필요(2개는 통신, 하나는 ssh)
- 도커 내부에서도 포트 관련 설정 필요한 것으로 보임(확인 )
<pre><code> docker run -it -p 00000:00 -p 00000:00 --name hail first.hail/ubuntu:20.04
</code></pre>

### 2-1) docker image start & attach
### 3) 
