import socket


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', PORT))
    server.listen(100)
    print("working")
    while True:
        client_socket, address = server.accept()
        process_requests(client_socket)


def process_requests(client_socket):
    while True:
        request_data = client_socket.recv(1024)
        response, is_answered = process_data(request_data)
        log_to_file(response)
        if is_answered:
            client_socket.send(response)
        # client_socket.close()


def log_to_file(data):
    with open('log.txt', 'ab+') as f:
        f.write(data)


def list_to_variables(data_list: list) -> tuple:
    sportsmen_number = data_list[0]
    channel = data_list[1]
    time = data_list[2]
    rounded_time = time[:7] + str(round(float(time[7:]), 1))
    group_number = data_list[3][:2]
    return sportsmen_number, channel, time, rounded_time, group_number


def process_data(request_data):
    data = request_data.decode('utf-8').rstrip('')
    sportsmen_data_list = data.split(' ')
    try:
        sportsmen_number, channel, time, rounded_time, group_number = list_to_variables(sportsmen_data_list)
    except (ValueError, IndexError):
        return b'Wrong data\n', True
    response_data = f'Спортсмен нагрудный номер {sportsmen_number} \
прошел отметку {channel} во время {rounded_time} \n'
    is_answered = False
    if group_number == '00':
        is_answered = True
    return response_data.encode('utf-8'), is_answered


PORT = 5556
start_server()


