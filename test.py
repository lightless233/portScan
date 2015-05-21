import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3.0)
address = ('104.236.171.163', 12)
sock.connect(address)
