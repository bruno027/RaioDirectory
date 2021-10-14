#!/usr/bin/python
import requests
import sys
import os
import platform
import argparse
import threading
import queue
from tqdm import tqdm

Fila = queue.Queue()


def print_banner():
	print("  ___      _       ___  _            _                ")
	print(" | _ \__ _(_)___  |   \(_)_ _ ___ __| |_ ___ _ _ _  _ ")
	print(" |   / _` | / _ \ | |) | | '_/ -_) _|  _/ _ \ '_| || |")
	print(" |_|_\__,_|_\___/ |___/|_|_| \___\__|\__\___/_|  \_, |")
	print("                                                 |__/ ")
	print("Feito por: Bruno Silva")



def parseargument():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--url', required=True, help='Qual o site? ex: http://example.com')
	parser.add_argument('-p', '--port', required=True, help='Qual a porta?')
	parser.add_argument('-w', '--wordlist', required=False, default='lista2.txt', help='Diretorio do wordlist' )
	parser.add_argument('-t', '--thread', required=False, default=1, type=int, help='Quantas Threads?')
	parser.add_argument('-e', '--extencao', required=False, help='Procurar por outras extencoes. Ex: -e php,jsf')
	args = parser.parse_args()

	try:
		requests.get(args.url+':'+args.port)
	except Exception as ex:
		print('O site %s:%s não existe' %(args.url,args.port))
		exit()
	try:
		arq = open(args.wordlist, 'r')
	except:
		print('Wordlist não localizada')
		exit()
	return args


def verificar_diretorios(url, port):
	while not Fila.empty():
		try:

			host = url+':'+port + '/' + Fila.get()

			cod = requests.get(host).status_code
			if cod != 404:
				print(host + ' ['+str(cod)+']')

		except:
			pass

def formar_wordlist(linhas,extencao):
	print('[*] Formando wordlist')
	ext = []
	for l in linhas:
		Fila.put(l.rstrip('\n'))

	if(extencao):
		try:
			ext = extencao.split(',')
		except:
			ext.append(extencao)
			pass
		for e in ext:
			for l in linhas:
				Fila.put(l.rstrip('\n')+'.'+e)
	print('[*] A wordlist foi formada')

def main():
	print_banner()
	args = parseargument()
	arquivo = open(args.wordlist, 'r')
	linhas = arquivo.readlines()
	arquivo.close()

	formar_wordlist(linhas,args.extencao)


	espera = []
	print('[*] Comecando a procurar diretorios')
	for i in range(0,args.thread):
		thread = threading.Thread(target=verificar_diretorios, args=(args.url, args.port))
		espera.append(thread)
		thread.start()



if __name__ == "__main__":
	main()


