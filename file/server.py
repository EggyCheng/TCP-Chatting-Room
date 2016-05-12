import socket

HOST = "" # accept everyone
PORT = 8051

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept() 
print("Connected by ", str(addr))

while 1:

	# listen for what client tells you to do
	raw_data = conn.recv(1024)
	data = repr(raw_data)[2:-1]
	print(data)
	print(raw_data)
	# if 'o' is pressed on client, send the file
	if (data == 'o'):
		with open ('index.png','rb') as f1:
			conn.send(f1.read(5000))
	
	# if 'q' is pressed on client, quit
	elif (data =='q'):
		break
