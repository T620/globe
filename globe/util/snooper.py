def getUserIP():
	import socket

	hostname = socket.gethostname()
	IP = socket.gethostbyname(hostname)

	return IP
