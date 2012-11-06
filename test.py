#!/usr/bin/env python

import simplejson

from tornado.ioloop import IOLoop

from torelp import ToRelpServer

class MyToRelpServer(ToRelpServer):
    def handle_syslog_message(self, msg):
        import pprint
        #pprint.pprint(msg)
        if msg['syslogtag'] == 'asterisk':
            if 'JSON:' in msg['msg']:
                notjson, json = msg['msg'].strip().split('JSON:')
                #pprint.pprint(json)
                pprint.pprint(simplejson.loads(json))
            

torelpserver = MyToRelpServer()
torelpserver.listen(20514)

IOLoop.instance().start()
