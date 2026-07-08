import io
import socket
import sys

class WSGIServer(object):
    address_family = socket.AF_INET #Expecting IPv4 adresses
    socket_type = socket.SOCK_STREAM #TCP
    request_queue_size = 1

    def __init__(self, server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(self.address_family, self.socket_type)
        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(server_address)
        listen_socket.listen(self.request_queue_size)

        # Get the server port and hostname
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        # Return headers set by Web framework/Web application
        self.headers_set = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            # New client connection
            self.client_connection, client_address = listen_socket.accept()
            # Handle one request, close the client connection then loop over and wait for another client connection
            self.handle_one_request()

    def handle_one_request(self):
        request_data = self.client_connection.recv(1024)
        self.request_data = request_data = request_data.decode('utf-8')

        # Print formatted request data like 'curl'
        print(''.join(f'<{line}\n' for line in request_data.splitlines()))
        self.parse_request(request_data)

        # Environment dictionary using request data
        env = self.get_environ()
        result = self.application(env, self.start_response)

        # Construct a response and send it back to the client
        self.finish_response(result)
