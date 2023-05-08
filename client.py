## CLIENT CODE ##

import socket
import threading
import random

# SERVER_HOST = '서버의 ip 주소를 입력하세요'
SERVER_HOST = '192.168.0.106'
SERVER_PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

def recv_data(client_socket):
    while True:
        data = client_socket.recv(2048)
        recv_msg = str(data.decode())
        print(recv_msg)

print('>> Connect Server')

# 서버에서 메세지를 받기 위한 thread 생성
recv_thread = threading.Thread(target=recv_data, args=(client_socket,), daemon=True)
recv_thread.start()

######################### server in peer ################################
# 자리 수마다 같은 숫자 중복없이 3자리 수 생성 (ex) 112 같이 1이 중복된 숫자 제외)
def generate_number():
    digits = random.sample(range(1,10), 3)
    number = digits[0] * 100 + digits[1] * 10 + digits[2]
    return str(number)

# count strike and ball
def count_strike_and_ball(answer, guess):
    strike = 0
    ball = 0
    for i in range(3):
        if answer[i] == guess[i]:
            strike += 1
        elif answer[i] in guess:
            ball += 1
    return strike, ball

# baseball game start
def run_game(peer_socket, peer_addr):
    # generate random number
    answer = generate_number()
    
    print('------- GAME START --------')
    print("answer = ", answer)
    
    while True:
        # when game start communication
        guess = peer_socket.recv(1024).decode()
        
        # game start를 위해 start를 입력받는다
        if guess == 'start':
            continue
        
        if not guess:
            continue
        
        print("guess = ", guess)
        # strike and ball 수 계산
        strike, ball = count_strike_and_ball(answer, guess)
        
        # 정답을 입력받았을 때
        if strike == 3 and ball == 0:
            print("answer " + str(peer_addr[0]) + " 3S 0B")
            break

        result = str(strike) + "S " + str(ball) + "B"
        send_answer = "answer " + str(peer_addr[0]) + " " + result
        print(send_answer)
        # strike & ball 수 답변하기
        peer_socket.send(send_answer.encode('utf-8'))
    
    print('------ GAME END -------')
    return

##### 클라이언트 내부에서 Thread로 돌아가고 있는 서버 #####
def handle_client_of_server(peer_socket, peer_addr):
    while True:
        data = peer_socket.recv(1024)
        # echo / peer끼리의 통신 확인
        peer_socket.send(data)
        
        # game start
        if data == b'start':
            run_game(peer_socket, peer_addr)
            # 정답 맞췄을 때
            end_msg = "3S 0B"
            peer_socket.send(end_msg.encode('utf-8'))

        if not data:
            continue
        
        # 연결된 peer에게 연결 종료 메세지를 보냄
        if data.split()[0] == b'disconnect':
            break
    
    print(">> peer communication end")
    print()
    peer_socket.close()
    
def start_server():
    client_of_server_host = '0.0.0.0'
    client_of_server_port = 12937
    
    client_of_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_of_server_socket.bind((client_of_server_host, client_of_server_port))
    client_of_server_socket.listen()
    
    print(">> client of server start")
    
    while True:
        peer_socket, peer_addr = client_of_server_socket.accept()
        # peer 끼리의 통신 성공 메세지
        comm_msg = ">> peer communication success!!"
        
        print()
        print(comm_msg)
        peer_socket.send(comm_msg.encode('utf-8'))
        
        # 각 peer 안에 서버 역할을 하는 thread를 생성해둔다
        peer_thread = threading.Thread(target=handle_client_of_server, args=(peer_socket,peer_addr), daemon=True)
        peer_thread.start()
        
# 클라이언트 내 서버 시작
peer_server_thread = threading.Thread(target=start_server, args=(), daemon=True)
peer_server_thread.start()
###############################################################

# 클라이언트에서 동작
while True:
    message = input()
    
    if message == '':
        continue
    
    # 서버에게 logoff 메시지를 보내서 연결을 종료한다
    if message == 'logoff':
        client_socket.send(message.encode())
        break
    
    # 서버에게 online_users 명령어를 보내서 online_user list를 받아온다.
    if message == 'online_users':
        client_socket.send(message.encode())
    
    # help 명령어를 통해 사용가능한 명령어 list 확인
    if message == 'help':
        print("                               < COMMAND LIST >")
        print(" --- communication with server --- ")
        print("   - online_users : send a request to the Server, get back a list of all online peers and display them on the screen")
        print("   - logoff : send a message to Server for logging off")
        print()
        print(" --- communication with peer --- ")
        print("   - connect [ip] [port] : request to play a game with the given IP and Port")
        print("   - disconnect [peer_ip] : end your game session with the listed peer")
        print("   - guess [peer_ip] [your guessing number] : send a guessing number to the peer that you've already initiated a game with via the 'connect' command")
        print("   - answer [peer_ip] [answer to the guess] : send a response to guessing number")
    
    # connect 명령어를 통해 게임을 하고자 하는 online_user와 연결하기
    if message.split()[0] == 'connect':
        peer_host = message.split()[1]
        peer_port = int(message.split()[2])

        peer_connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_connect_socket.connect((peer_host, peer_port))
        
        # communication success messages receive
        print()
        print(peer_connect_socket.recv(1024).decode())
        
        print("enter 'start' to start baseball game with peer")

        # connect 명령어를 통해 peer와 연결한 상태
        while True:
            # 메시지 전송 및 수신
            message = input()

            peer_connect_socket.send(message.encode('utf-8'))
            response = peer_connect_socket.recv(1024)
            print('peer echo:', response.decode())

            # 연결된 peer와 연결 끊기 
            if message.split()[0] == 'disconnect':
                peer_connect_socket.send(message.encode('utf-8'))
                response = peer_connect_socket.recv(1024)   
                peer_connect_socket.close()
                print('>> peer communication end')
                break
            
            # start를 입력하여서 숫자야구 게임 시작하기
            if message == 'start':
                peer_connect_socket.send(message.encode('utf-8'))
                print(" ----- GAME START ------ ")
                print("To send your guess 3-digit number to peer : 'guess peer_ip guess_num'")
                
                while True:
                    # 'guess peer_ip guess_num' 형태로 추측한 숫자 입력하기
                    guess_command = input()
                    
                    guess_num = guess_command.split()[2]
                    if guess_command.split()[0] == 'guess':
                        # send guess_num
                        peer_connect_socket.send(guess_num.encode('utf-8'))
                    
                    # receive result
                    curr_state = peer_connect_socket.recv(1024)
                    print("peer_response = ", curr_state.decode())

                    # 3S로 정답 맞췄을 때 게임 종료
                    if curr_state == b'3S 0B':
                        print('----------------------')
                        print("YOU WIN !! game over !!")
                        print("----- GAME END -------")
                        print("enter 'disconnect peer_ip' if you want to disconnect with peer")
                        print()
                        break
                
                # game over되면 그냥 peer 끼리의 연결된 상태로 바뀜(disconnect 명령어 입력해야지 peer와의 연결이 끊김)
                continue
    print()

# 서버와의 연결 종료
client_socket.close()
