#!/usr/bin/python
#coding=utf-8

import socket, sys
import getopt
import threading, Queue

# 全局变量
gIP = ""		# target IP
gPort = []		# target Port
gMethod = []	# Scan Method
gThread = 10	# scan thread number
gTimeout = 3.0	# time out
gPortqueue = Queue.Queue(maxsize = 65536)	# port queue
gOpenPort = []
glock = threading.Lock()

def usage():
	print 'this is usage'

def ip_check(ip):
	q = ip.split('.')
	return len(q) == 4 and len(filter(lambda x: x >= 0 and x <= 255, \
		map(int, filter(lambda x: x.isdigit(), q)))) == 4


def scan():
	for scanMethod in gMethod:
		if scanMethod == 'T':
			# TCP 扫描
			if glock.acquire():
				if not gPortqueue.empty():
					port = gPortqueue.get()
					glock.release()
				else:
					glock.release()
					return
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(gTimeout)
			address = (gIP, port)
			try:
				sock.connect(address)
			except:
				sock.close()
				continue
			if glock.acquire():
				print 'Port: ', port, '\t opened'
				glock.release()
			sock.close()
			gOpenPort.append(port)

def main():
	#global gIP, gPort, gMethod, gThread, gPortqueue
	print 'Target IP: ', gIP
	print 'Target Port: ',gPort
	if not gMethod:
		gMethod.append('T')
	print 'Scan Method', gMethod

	if not ip_check(gIP):
		print 'Invalid IP address!!'
		sys.exit(0)
	# 将端口放到队列中，为后续的多线程扫描做准备
	for i in gPort:
		gPortqueue.put(i)

	# print "------ Result ------"
	# print "IP: ", gIP
	# for t in xrange(1):
	# 	t = threading.Thread(target=scan)
	# 	t.setDaemon(True)
	# 	t.start()
	# 	t.join()

	# 判断扫描方法
	for scanMethod in gMethod:
		if scanMethod == 'T':
			# TCP 扫描
			print 'TCP scan start!'
			print '------ Result ------'
			print 'IP: ',gIP

			for port in gPort:
				# print '[*] Scanning port: ', port
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout(gTimeout)
				address = (gIP, port)
				# print address
				try:
					sock.connect(address)
				except:
					#print 'close'
					sock.close()
					continue
				sock.close()
				gOpenPort.append(port)
				print 'Port: ', port, ' opened'

if __name__ == '__main__':
	# 解析参数
	try:
		opts, args = getopt.getopt(sys.argv[1:],'ht:p:n:T')
	except Exception, e:
		print e
		usage()
		sys.exit(0);

	for o, a in opts:
		if o in ('-h','--help'):
			usage();
			sys.exit(0)
		elif o in ('-t','--target'):
			gIP = a
		elif o in ('-p','--port'):
			# 解析端口号
			if '-' in a and ',' in a:
				pass
			elif '-' in a:
				tPort = a.split('-')
				portStart = int(tPort[0],10)
				portEnd = int(tPort[1],10)
				if portStart > portEnd:
					portStart, portEnd = portEnd, portStart
				if portStart <= 0 or portEnd <= 0:
					print u"Invalid Port!"
					sys.exit(0)
				i = portStart
				#print portStart,portEnd
				while i <= portEnd:
					gPort.append(i)
					i += 1
			elif ',' in a:
				tPort = a.split(',')
				for port in tPort:
					gPort.append(int(port))
			else:
				gPort.append(a)
		elif o in ('-n','--number'):
			pass
		elif o in ('-T','--TCP'):
			pass
		else:
			usage()
			sys.exit(0)
	main()





