import socket
from pathlib import Path

from utils import ask_port


DEFAULT_HOST = 'localhost'
EXIT = 'exit'


def send(sock, data):
    length = '{:0>3}'.format(len(data))
    sock.send((length + data).encode())
    if data:
        print(f'Вы отправили данное количество символов: {int(length)}.')


def recv(sock):
    data = sock.recv(1024).decode()
    length = data[:3]
    if data:
        print(f'От сервера получено данное количество символов: {int(length)}.')
    return data[3:]


def _main():
    host = input('Введите имя хоста, -1 для значения по умолчанию: ')
    if host == '-1':
        host = DEFAULT_HOST
    port = ask_port()

    sock = socket.socket()
    sock.connect((host, port))

    while True:
        command = recv(sock)
        if command == '!get_token':
            if not Path('token.txt').is_file():
                Path('token.txt').touch()
            token = Path('token.txt').read_text()
            if token:
                send(sock, Path('token.txt').read_text())
            else:
                send(sock, str(None))
        elif command == '!save_token':
            Path('token.txt').write_text(recv(sock))
        elif command == '!password':
            send(sock, input('Пароль: '))
        elif command == '!username':
            send(sock, input('Имя: '))
        elif command == '!success':
            print(recv(sock))
            while True:
                message = input()
                if message == EXIT:
                    break
                send(sock, message)
                data = recv(sock)
                print(data)
            break
        elif command == '!forbidden':
            print('Неверный пароль.')
            break

    sock.close()


if __name__ == '__main__':
    _main()