# DC_Termproject
> P2P baseball game with napster-style server  

peer들의 정보(ip address & port)를 저장하고 있는 서버를 한 대 두고   
서버에서 온라인 상태의 peer정보를 받아와 peer끼리 서로 연결을 한 뒤 숫자야구 게임을 진행한다.

## 개발 환경
```sh
OS : Ubuntu 20.04.5 LTS
language : python 3.8.10
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
disconnect [peer_ip]                 # end your game and disconnect with peer
```

## 사용 예제

```sh
##### communication with server
help                                   # to notify commands
online_users                           # to notify online peers infomation

connect [peer_ip] [port]               # connect peer who you want to game


##### commuication with peer
# when connection success with peer
start                                  # to start 3-digit baseball game
guess [peer_ip] [guessing number]      # send message with your 3-digit guessing number

# when correct and game over with peer
start                                  # if you want to start again
disconnect [peer_ip]                   # to end game and disconnect with peer


##### communication with server
# when you want to game another online peer
connect [peer_ip] [port]               # connect and play game with another peer

# when you want to logging off
logoff                                 # send message to server for loging off 
```

## 주의 사항
- ctrl-C 에 의한 종료도 online_peers 명단에서 제외된다.
- connect & guess 명령어를 사용할 때는 반드시 주어진 명령어 형식대로 입력해주어야 한다.
  - error가 발생한다.
  - 이 경우 연결된 peer 모두 종료하고 다시 시작 해주어야 한다.

## 정보

201911523 이민선
