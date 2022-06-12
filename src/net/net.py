import socket
import logging


def host_ip2():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def host_ip():
    try:
        hostname = socket.gethostname()
        hostname_s = hostname.split("-")
        if len(hostname_s) >= 5:
            hostname = "-".join(hostname_s[:-1])
        ip = socket.gethostbyname(hostname)
        return ip
    except Exception as e:
        logging.debug(f"host_ip:{e}, try to host_ip2")
        return host_ip2()
