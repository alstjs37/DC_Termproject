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

## command of client

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
help                                   # to recognize commands
online_users                           # to recognize online peers infomation

connect [peer_ip] [port]               # connect peer who you want to game


##### commuication with peer
# when connection success with peer
start                                  # to start 3-digit baseball game
guess [peer_ip] [guessing number]      # send message with your 3-digit guessing number

### 게임이 종료된거긴 하지만 아직 peer와의 연결이 끊긴 상태가 아니다. 
### peer와의 연결 종료를 위해서는 disconnect 명령어를 사용해야 한다.
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
- 'ctrl-c' 에 의한 종료도 online_peers 명단에서 제외된다.
- connect & guess 명령어를 사용할 때는 반드시 주어진 명령어 형식대로 입력해주어야 한다.
  - error가 발생한다.
  - 이 경우 연결된 peer 모두 종료하고 다시 시작 해주어야 한다.
- 같은 공유기를 사용하여 내부망 ip를 통해 연결할 때는 port-forwarding 하지 않아도 된다.
- 만약 다른 공유기에 물려있거나 외부 ip를 사용할 때는 code에서 지정한 port_num(12937)으로 port-forwarding 해주어야 한다.

## 정보

201911523 이민선
