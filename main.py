#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import zbar
import sys

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

spc = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a')
spc.write("""network = {
	ssid="%s"
	psk="%s"
}
""" % (essid, pw))
spc.close()
