import socket

IPAddress='10.209.68.57'
Port=8000

print('Connecting via ethernet')
connectionType = 'Ethernet'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5) # sets the timeout of the receive command. 
server_address = (IPAddress, Port) #IP address, port
sock.connect(server_address)

commandString = "PR1\r\n"

sock.sendall(commandString.encode())
response_raw = sock.recv(100)
response_strip = response_raw.strip()

print(response_strip)

ascii_ack = b'\x06'
if response_raw.strip() == ascii_ack:
    print("ACK")


commandString = "\x05\r\n"
sock.sendall(commandString.encode())
response_raw = sock.recv(100)
b, response, r_end = response_raw[:2], response_raw[2:len(response_raw)-3], response_raw[len(response_raw)-3:]
print(response_raw)
print(b)
print(response.decode('utf-8').strip())
print(r_end)
print(float(response.decode('utf-8').strip()))



# # Convert to string representation and strip unwanted characters
# stripped_value = response_raw.strip(b'\r\n')

# # Format the result to match 'x06'
# formatted_value = f'x{stripped_value}'

# print(formatted_value)