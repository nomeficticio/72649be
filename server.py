from socket import *
from datetime import datetime
import os
import re



#ESSE CÓDIGO É SÓ UM EXEMPLO. VOCê PODE MELHORAR O CÓDIGO DE VÁRIAS FORMAS.

s = socket(AF_INET, SOCK_STREAM)
s.bind(('localhost', 5000))
s.listen(1)


#Headers para o browser entender a requisição.
def response(text):
    obj.send(b"HTTP/1.1 200 OK\r\n")
    obj.send(b"Content-Type: text/html\r\n\r\n")
    obj.send(text.encode())
    obj.send(b"\r\n\r\n")
    obj.close()

print('Running...')
while True:
    obj, addr = s.accept()

    try:
        while obj:
            req = obj.recv(2048).decode()

            #Vai procurar o tamanho do coteudo nos headers. isso é o grupo 1: ([0-9]+)
            length = re.search(r'Content-Length: ([0-9]+)', req)

            buffer = b""

            if length:
                length = int(length.group(1))

                while len(buffer) < length:
                    buffer += obj.recv(length)

            
            # A variavel inf vai receber as informaçoes da imagem, e a variavel *data (com simbolo: *) vai receber todo o resto como uma lista.
            inf, *data = buffer.decode("iso-8859-1").split("\r\n\r\n")

            tmp_name = re.search(r'filename="(.*[.]\w+)"', inf)

            if tmp_name:
                #Atribui um novo nome para a imagem.
                filename = "uploads/" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S-") + tmp_name.group(1)

                #Verifica se o diretorio uploads existe. ou cria.
                if not os.path.isdir("uploads"):
                    os.makedirs("uploads")

                #Vai converter a lista em string e depois para bytes.
                file = ''.join(map(str, data)).encode('iso-8859-1')

                with open(filename, 'wb') as up_file:
                    up_file.write(file)

                response("<h1>Success</h1>")

            else:
                response("<h1>File is mandatory.</h1>")
                

    except Exception as ex:
        print(ex)
        obj.close()
