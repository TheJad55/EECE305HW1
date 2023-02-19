import socket
import time
import re 
def main():
    # Set up the socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(('0.0.0.0', 5023))
    proxy_socket.listen(1)
    print("Proxy server is waiting for a request on port 5023...")

    # Accept incoming connections
    while True:
        client_socket, client_address = proxy_socket.accept()
        print("Received incoming connection from", client_address)

        # Receive request from client
        request = client_socket.recv(4096).decode()
        print("Received request:", request)
        request_time = time.time()

        # Parse the request to get the destination server IP address
        destination_ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', request).group()
        print("Destination IP address:", destination_ip)

        # Send request to destination server
        try:
            destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            destination_socket.connect((destination_ip, 80))
            destination_socket.sendall(request.encode())
            print("Sent request to destination server at", time.time() - request_time, "seconds")

            # Receive response from destination server
            response = destination_socket.recv(4096)
            print("Received response from destination server at", time.time() - request_time, "seconds")

            # Send response back to client
            client_socket.sendall(response)
            print("Sent response to client at", time.time() - request_time, "seconds")
        except:
            print("Error: Unable to connect to destination server.")
            client_socket.sendall("Error: Unable to connect to destination server.".encode())

        # Close sockets
        client_socket.close()
        destination_socket.close()
# Call the function
main()