## SERVER CODE ##

import socket
from _thread import *

client_sockets = []
# 현재 서버에 접속해 있는 peer ip & port info 저장해두는 list
online_peer_info = []

## Server IP and Port ##
HOST = '0.0.0.0'
PORT = 9999

# client와 연결할 때마다 새로운 thread를 통해 연결해준다
def threaded(client_socket, addr):
    # 연결된 client의 정보 출력
    print('>> Connected by :', addr[0], ':', addr[1])
    
    # 연결한 client에게 본인의 clinet ip 정보를 제공
    your_info = "INFO -> " + "your ip address : " + str(addr[0])
    client_socket.send(your_info.encode('utf-8'))
    
    # 접속한 클라이언트의 주소, 포트 tuple형태로 list에 저장해두기
    info = (addr[0], addr[1])
    online_peer_info.append(info)
    
    # 현재 접속해 있는 peer 수 출력
    print("현재 접속해 있는 peer 수 : ", len(online_peer_info))
    print()
    
    # client가 disconnect 할 때까지 계속 진행되는 코드
    while True:
        try:
            # 메세지 받기
            data = client_socket.recv(1024)
            
            # ctrl-c(에러)로 종료했을 때 peer정보 삭제해주기
            if not data:
                print('error interrupt -> disconncected')
                # online_peer_info list에서 disconnected 된 peer 정보 지우기
                for out_peer in online_peer_info:
                    if(out_peer[0] == addr[0] and out_peer[1] == addr[1]):
                        online_peer_info.remove((out_peer[0], out_peer[1]))
                        
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                print("현재 접속해 있는 peer 수 : ", len(online_peer_info))
                print()
                break

            # online_users 명령어 받았을 때, 명령어 보낸 peer에게만 online users의 정보 보내주기
            for client in client_sockets:
                if client == client_socket:
    
                    # online_users 명령어 입력받았을 때
                    if data.decode() == 'online_users':
                        client.send(" --- online users list --- ".encode())
                        send_msg = ""
                        
                        for i, peer in enumerate(online_peer_info):
                            online_peer_str = str(i+1) + " : ip = " + str(peer[0]) + " port = " + str(12937) +'\n'
                            send_msg += online_peer_str
                            
                        # online_users 정보 보내기
                        client.send(send_msg.encode())
            
            # logoff 명령어 받았을 때
            if data.decode() == 'logoff':
                # 더이상 online 상태가 아니므로 peer정보는 삭제하기
                for out_peer in online_peer_info:
                    if(out_peer[0] == addr[0] and out_peer[1] == addr[1]):
                        online_peer_info.remove((out_peer[0], out_peer[1]))
                        
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                print("현재 접속해 있는 peer 수 : ", len(online_peer_info))
                print()
                break
                
        except ConnectionResetError as e:
            break
    
    # 연결 종료
    client_socket.close()

# socket create & bind & listen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
print('>> Server Start ')
print('>> Server listening')


# client와 연결
try:
    while True:
        # client socket과 server socket connection
        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        
        # new client, new thread
        start_new_thread(threaded, (client_socket, addr))
        
except Exception as e:
    print('에러 : ', e)

finally:
    server_socket.close()