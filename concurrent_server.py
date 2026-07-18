import os
import socket
import time 
import signal
import errno 

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def zombies(signum, frame):
    pid, status = os.wait()
    print('Child {pid} terminated with status {status}'
          '\n'.format(pid = pid, status = status))


def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_response = b"""\
HTTP/1.1 200 OK 

Hello !!
"""
    client_connection.sendall(http_response)
    # Sleep to allow the parent to loop over to accept and block
    time.sleep(3)

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port}...'.format(port = PORT))
    # print('Parent PID (PPID): {pid}\n'.format(pid = os.getpid()))

    signal.signal(signal.SIGCHLD, zombies)

    while True:
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args 
            if code == errno.EINTR:
                continue 
            else: 
                raise

        pid = os.fork() # When a parent forks a new child, the child process gets a copy of the parent's file descriptors
        if pid == 0: # Child
            listen_socket.close() # Clise child copy!!
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:
            client_connection.close() # Close parent copy and loop over

if __name__ == '__main__':
    serve_forever()
