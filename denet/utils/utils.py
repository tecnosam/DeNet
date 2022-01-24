import socket


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        ip = st.getsockname()[0]
    except OSError:
        ip = '127.0.0.1'

    return ip


def setup_server_socket(port: int):
    _server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _server.bind((extract_ip(), port))

    return _server


def setup_client_socket(host, port):
    try:
        _client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _client.connect((host, port))

        return _client
    except OSError as e:
        _client = None

    return _client
