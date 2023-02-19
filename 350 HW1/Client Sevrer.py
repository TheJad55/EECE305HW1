import socket
import time
import uuid

def get_mac_address():
# Generates a unique identifier for the network interface of the machine that this script is running on
    mac_address = uuid.getnode()
    return ':'.join(("%012X" % mac_address)[i:i+2] for i in range(0, 12, 2))

# User enters website IP
destination_ip = input("Enter the website IP you want to access: ")

# Create a socket for communication with the proxy server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect client server to proxy server
proxy_ip = "127.0.0.1" # Set to the IP of your proxy server
proxy_port = 5023 # Set to the port of your proxy server
try:
    # Connect to proxy server
    client_socket.connect((proxy_ip, proxy_port))
except ConnectionRefusedError:
    # Display error if connection was not established
    print("Error: Unable to connect to proxy server at", proxy_ip, ":", proxy_port)
    client_socket.close()
    exit()

# Send the request to the proxy server
request = "GET http://" + destination_ip + " HTTP/1.1\r\nHost: " + destination_ip + "\r\nConnection: close\r\n\r\n"
start_time = time.time()
client_socket.send(request.encode())
print("Request sent to proxy server at", time.ctime(start_time))

# Receive the data from the proxy server
try:
    response = client_socket.recv(4096)
except ConnectionResetError:
    print("Error: Connection to proxy server was reset.")
    client_socket.close()
    exit()
end_time = time.time()
print("Response received from proxy server at", time.ctime(end_time))

# Display the data receieved to the user
print("\nResponse:")
print(response.decode())

# Calculate and display the total round-trip time
round_trip_time = end_time - start_time
print("\nTotal round-trip time:", round_trip_time, "seconds")

# Display the MAC address of the client's physical machine
mac_address = get_mac_address()
print("\nMAC address:", mac_address)

# Close the socket
client_socket.close()
