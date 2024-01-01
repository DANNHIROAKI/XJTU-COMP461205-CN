import threading
import socket
import sys
import os

# data
exit_flag = False
proof_flag = False
recv_flag = True

def wait_for_exit(sock):
    global exit_flag, proof_flag
    while True:
        if exit_flag:
            sock.close()
            os._exit(0)
            break
    return

def CS_Server(sock, addr):
    global exit_flag, proof_flag, recv_flag
    proof_flag = False
    while True:
        try:
            if exit_flag:
                return
            data, addr = sock.recvfrom(1024)
            data = data.decode('utf8')
            if(proof_flag):
                print('服务器:', data)
                recv_flag = True
                sys.stdout.flush()
            else:
                print(data, end='')
                sys.stdout.flush()
            if(data == '信息正确!\r\n'):
                proof_flag = True
                print('客户端: ', end='')
                sys.stdout.flush()
        except:
            pass

def CS_Client(sock, addr):
    global exit_flag, proof_flag, recv_flag
    while True:
        try:
            if(proof_flag):
                while(recv_flag == False):
                    pass
                data = input('客户端: ')
                recv_flag = False
            else:
                data = input('')
                recv_flag = False
        except:
            continue
        sock.sendto(data.encode('utf8'), addr)
        if(data == 'exit'):
            exit_flag = True
            return
        

# main
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
port = 1212
# client_socket.connect((host, port))
client_socket.sendto('Hello!'.encode('utf8'), (host, port))
print("Connect Succeed!")
sys.stdout.flush()
threading.Thread(target=wait_for_exit, args=(client_socket, )).start()
threading.Thread(target=CS_Server, args=(client_socket, (host, port))).start()
threading.Thread(target=CS_Client, args=(client_socket, (host, port))).start()
