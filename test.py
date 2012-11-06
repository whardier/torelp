#!/usr/bin/env python

import pprint
import simplejson

from tornado.ioloop import IOLoop

from torelp import ToRELPServer

class MyToRELPServer(ToRELPServer):
    def handle_syslog_message(self, msg):
        if msg['syslogtag'] == 'jsontest':
            if 'JSON:' in msg['msg']:
                notjson, json = msg['msg'].strip().split('JSON:')
                pprint.pprint(simplejson.loads(json)) #This is just an example

torelpserver = MyToRELPServer()
torelpserver.listen(20514)

IOLoop.instance().start()
