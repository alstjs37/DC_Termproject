# DC_Termproject
> P2P baseball game with napster-style server

peer들의 정보(ip address & port)를 저장하고 있는 서버를 한 대 두고 그 서버에서 온라인 상태의 peer정보를 받아와
peer끼리 서로 연결을 한 뒤 숫자야구 게임을 진행한다.

## 개발 환경
```sh
OS : Ubuntu 20.04.5 LTS
python3 : python 3.8.10
```

## 설치 방법

Linux :

```sh
git clone https://github.com/alstjs37/DC_Termproject.git
```

## 실행 방법

Server :

```py
python3 -u server.py
```

client :

```py
python3 -u client.py
```

## command in client

#### when client communication with server :
```sh
help                                 # to lookup command (display all possible commands and their description)
online_users                         # send a request to the server, get back a list of all online peers and display them on the screen
logoff                               # send a message to server for logging off
```

#### when client communication with peer :
```sh
connect [ip] [port]                  # request to play a game with the given IP and port
start                                # send a message to peer to start baseball game
guess [peer_ip] [guessing number]    # send a guessing number to the peer
answer [peer_ip] [answer to guess]   # send a response to guessing number (automatically)
disconnect [peer_ip]                 # end your game session with peer
```

## 정보

201911523 이민선
