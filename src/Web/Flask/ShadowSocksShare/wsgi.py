#!/usr/bin/env python
import os
from app import app as application

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    httpd.serve_forever()

