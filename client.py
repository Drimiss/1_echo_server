import socket

IP = input('Введите ip адрес для подключения(значение по умолчанию - 127.0.0.1): ')
if IP == '':
    IP = '127.0.0.1'

port = input('Введите порт для подключения(значение по умолчанию - 12345): ')
if port == '':
    port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, port))
print(f'Соединение Успешно!')
try:
    while True:
        message_from_server = client_socket.recv(1024).decode()
        print(f'Получено от сервера: {message_from_server}')

        message_from_client = input('Введите текст для отправки: ')

        client_socket.sendall(message_from_client.encode())
        print(f'Отправлено: {message_from_client}')

        if message_from_client == 'exit':
            break
except:
    print('ОЙ,что-то пошло не так, попробуйте снова(')
    client_socket.close()
client_socket.close()