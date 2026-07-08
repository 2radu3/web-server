import socket

HOST, PORT = '', 8888

#Creating a new socket object.
#AF_INET to use standard IPv4 adresses
#SOCK_STREAM for TCP
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Overriding the opening cooldown.
listen_socket.bind((HOST, PORT)) #Assigning the socket to the host IP and port.
listen_socket.listen(1) #Queue size
print(f'Serving HTTP on port {PORT}...')

while True: # Starts accepting new connections in a loop
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024) #Reads data sent by the client (max 1024 bytes at a time).
    print(request_data.decode('utf-8')) #The data we get is in raw bytes so we need to decode it so that it can be printed to the console.

    #Converts the response string into bytes.
    http_response = b"""\ 
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response) #Sends the response bytes back to the client.
    client_connection.close()

# telnet lcoalhost 8888 -> To setup a TCP connection.
# GET /hello HTTP/1.1 -> To send an HTTP GET request and get back a response.