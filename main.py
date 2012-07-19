#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import zbar
import sys

wstemplate = """network = {
	ssid="%s"
	psk="%s" 
}
"""

if len(sys.argv) > 2:
	print "Der Ort der Konfigurationsdatei von wpa_supplicant ist - wenn überhaupt - das einzige Argument!"
	exit(1)
elif len(sys.argv) == 2:
	wsconf = sys.argv[1]
else:
	wsconf = '/etc/wpa_supplicant/wpa_supplicant.conf'

reessid = re.compile(r"S:(\w+)")
repw    = re.compile(r"P:(\w+)")

proc = zbar.Processor()
proc.parse_config('enable')
proc.init('/dev/video0')
proc.visible = True
proc.process_one()
proc.visible = False

for symbol in proc.results:
	matchessid = re.search(reessid, symbol.data)
	matchpw    = re.search(repw, symbol.data)
	if (matchessid != None) & (matchpw != None):
		essid = matchessid.group(1)
		pw = matchpw.group(1)
		break

spc = open(wsconf, 'a')
spc.write(wstemplate % (essid, pw))
spc.close()
