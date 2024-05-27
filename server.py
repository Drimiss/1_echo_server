import socket
import logging

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',encoding='utf-8')

def start_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            sock.bind((host, port))
            break
        except OSError:
            logging.info(f'Порт {port} уже занят, пробуем следующий порт...')
            port += 1

    sock.listen(1)
    logging.info(f'Сервер запущен на {host}:{port}')
    print('Сервер запущен')

    while True:
        logging.info('Ожидание подключения клиента...')
        client_socket, client_address = sock.accept()
        client_ip = client_address[0]
        logging.info(f'Подключен клиент {client_address}')

        client_name = get_client_name(client_ip)

        if not client_name:
            client_socket.sendall('Введите имя: '.encode())
            client_name = client_socket.recv(1024).decode().strip()
            logging.info(f'Клиенту {client_address} присвоено имя {client_name}')

            with open('client_base.txt', 'a') as file:
                file.write(f'{client_ip},{client_name}\n')

        welcome_message = f'Добро пожаловать, {client_name}!'
        client_socket.sendall(welcome_message.encode())

        while True:
            data = client_socket.recv(1024)

            input_data = data.decode()
            logging.info(f'{client_name}: {input_data}')

            if input_data.strip().lower() == 'exit':
                break

            client_socket.sendall(data)
            logging.info(f'{client_name}: {input_data}')

        logging.info(f'Клиент {client_name} покинул нас')
        client_socket.close()
    
    sock.close()

def get_client_name(client_ip):
    with open('client_base.txt', 'r') as file:
        for line in file:
            ip, name = line.strip().split(',')
            if ip == client_ip:
                return name

IP = input("Введите IP-адрес сервера(по умолчанию 127.0.0.1): ")
if IP == '':
    IP = "127.0.0.1"

port = input('Введите порт для внешнего подключения(по умолчанию 12345): ')
if port == '':
    port = 12345

start_server(IP, port)