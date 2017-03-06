#!/usr/bin/python

"""
Authors
Domenico Scotece
Michele Solimando
"""

import socket

class socketClass:
    #Costruttore della socket
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    #Funzione di connessione della socket
    def connect(self, host, port):
        self.sock.connect((host,port))

    #Funzione invio dei messaggi
    def sendMessage(self, msg):
        amount_received=0
        amount_expected = len(msg)
        while amount_received < amount_expected:
            sent = self.sock.send(msg[amount_received:])
            if sent == 0:
                raise RuntimeError
            amount_received += sent


    #Funzione ricezione messaggi
    def receiveMessage(self):
        msg=''