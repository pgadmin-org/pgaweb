##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import socket

import pgaweb.settings as settings


def varnish_ban(url='/'):
    if settings.VARNISH_HOST is None or settings.VARNISH_HOST == '':
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((settings.VARNISH_HOST, 80))
    except socket.error:
        pass
    else:
        request = "PURGE {} HTTP/1.1\r\nHost: {}\r\n\r\n".\
            format(url, settings.VARNISH_HOST)

        sock.sendall(request.encode())

        response = sock.recv(1024)

        http_status, body = response.decode("utf-8").split("\n", 1)
        _, status, text = http_status.split(" ", 2)

        if status == "%s" % 200:
            pass
    finally:
        sock.close()
