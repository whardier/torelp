ToRELP
======

Tornado based RELP server

Setup
=====

The test script uses port 20514

On rsyslog we want to put the following in place:

```
$ModLoad omrelp

$WorkDirectory /var/spool/rsyslog  # default location for work (spool) files

$ActionQueueType LinkedList   # use asynchronous processing
$ActionQueueFileName localhost # set file name, also enables disk mode
$ActionResumeInterval 1    # infinite retries on insert failure
$ActionResumeRetryCount -1    # infinite retries on insert failure
$ActionQueueSaveOnShutdown on # save in-memory data if rsyslog shuts down

*.* :omrelp:localhost:20514;RSYSLOG_ForwardFormat
```

Why?
====

New cool message queue using reliable messaging services that is simple to configure

How?
====

Check out ```test.py```.  Just inherit the ToRELPServer class and override the class method ```handle_syslog_message```.

Todo
====

Add URL style dispatcher
Add datetime parser
Add new inbound formats
Add plain TCP syslog support
