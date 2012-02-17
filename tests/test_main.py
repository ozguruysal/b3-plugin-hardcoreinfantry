# -*- encoding: utf-8 -*-
from tests import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

import os
import time
import b3
from b3.fake import fakeConsole
from hardcoreinfantry import HardcoreinfantryPlugin

p = HardcoreinfantryPlugin(fakeConsole)
p.onLoadConfig()
p.onStartup()

print "----------------------------Rcon console test"
fakeConsole._serverConnection.connected = True

time.sleep(5)

p._delay = 15

print "----------------------------Should disable vehicles"
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_WARMUP, None))

time.sleep(1)

print "----------------------------Should enable vehicles"
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_START, None))