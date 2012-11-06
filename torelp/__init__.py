#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""torelp"""

__name__ = "torelp"
__author__ = 'Shane R. Spencer'
__email__ = "shane@bogomip.com"
__license__ = 'MIT'
__copyright__ = '2012 Shane R. Spencer'
__version__ = '0.0.1'
__status__ = "Prototype"

import sys
from tornado.netutil import TCPServer

import re

RSYSLOG_FORWARD_FORMAT = re.compile(r'<(?P<pri>\w+)>(?P<rfc3339>\S+) (?P<hostname>\S+) (?P<syslogtag>\S+): (?P<msg>.*)')
RSYSLOG_FORWARD_FORMAT_PID = re.compile(r'<(?P<pri>\w+)>(?P<rfc3339>\S+) (?P<hostname>\S+) (?P<syslogtag>\S+)\[(?P<pid>\w+)\]: (?P<msg>.*)')

class ToRelpServer(TCPServer):
    def handle_stream(self, stream, address):
        ToRelpConnection(stream, address, server=self)

    def handle_syslog_message(self, message):
        """ Override Me """

class ToRelpConnection(object):

    def __init__(self, stream, address, server):
        self.stream = stream
        self.address = address
        self.server = server

        self._buffer = ''
        self._on_read('')

    def _on_read(self, line):
        self._buffer += line

        id = 0
        command = ''
        length = 0
        data = ''

        if line:
            try:
                id, command, length, data = self._buffer.strip('\n').split(' ', 3)
                id = int(id)
                length = int(length)
            except:
                pass

            try:
                id, command, length = self._buffer.strip('\n').split(' ', 3)
                id = int(id)
                length = int(length)
            except:
                pass

            if not len(data) == (length):
                id = 0

            if id and command:
                self._buffer = ''   
                self._process(id, command, length, data)


        if not self.stream.closed():
            self.stream.read_until('\n', self._on_read)

    def _process(self, id, command, length, data):

        if command == 'open':            
            self.stream.write('%s rsp %d 200 OK\n%s\n' % (id, len(data) + 7, data))
        elif command == 'close':
            self.stream.write('%s rsp 0\n' % id)
            self.stream.write('0 serverclose 0\n')
            self.stream.close()
        elif command == 'syslog':
            self._handle_syslog(data)
            self.stream.write('%s rsp 6 200 OK\n' % id)
        else:
            self.stream.write('%s rsp 6 200 OK\n' % id)

    def _handle_syslog(self, data):
        msg = re.match(RSYSLOG_FORWARD_FORMAT_PID, data)
        if not msg:
            msg = re.match(RSYSLOG_FORWARD_FORMAT, data)
        if msg:
            self.server.handle_syslog_message(msg.groupdict())
