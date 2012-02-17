# -*- coding: utf-8 -*-
#
# Hardcore Infantry Only BF3 Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2012 Freelander (freelander@fps-gamer.net)
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# CHANGELOG
#
# 0.1   - Initial release

__version__ = '0.1'
__author__  = 'Freelander'

import b3
import b3.events
from b3.plugin import Plugin
import threading

class HardcoreinfantryPlugin(Plugin):

    requiresConfigFile = False

    def __init__(self, console, config=None):
        self._delay = 40
        Plugin.__init__(self, console, config)
        wait_for_rcon_crontab = None

################################################################################################################
#
#    Plugin interface implementation
#
################################################################################################################

    def startup(self):
        '''Initialize plugin settings'''
        # Register our events
        self.registerEvent(b3.events.EVT_GAME_WARMUP)
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        # Add crontab to check if rcon console is functional so we can do stuff after
        self.wait_for_rcon_crontab = b3.cron.PluginCronTab(self, self.check_if_rcon_is_ready, second='*/5')
        self.console.cron + self.wait_for_rcon_crontab

    def onEvent(self, event):
        '''Handle intercepted events'''
        if event.type == b3.events.EVT_GAME_ROUND_START:
            # starting a new thread to enable vehicles again
            t = threading.Timer(self._delay, self.toggle_vehicle_status, ['true'])
            t.start()
        elif event.type == b3.events.EVT_GAME_WARMUP:
            self.toggle_vehicle_status('false')

    def onRconReady(self):
        '''Rcon connection is ready now'''
        self.info("Rcon is ready")
        self.apply_hardcore_settings()

################################################################################################################
#
#    Other methods
#
################################################################################################################

    def toggle_vehicle_status(self, status):
        '''Enables or disables vehicles'''
        try:
            self.console.setCvar('vehicleSpawnAllowed', status)
            self.debug('Setting vehicle status to %s' % status)
        except CommandFailedError, err:
            self.debug("Cannot change vehicle status : %s" % err.message)

    def check_if_rcon_is_ready(self):
       '''Checks if rcon console is ready for use and calls onRconReady method if ture'''
       self.debug('Checking frostbite2 connection...')
       if hasattr(self.console._serverConnection, 'connected') and self.console._serverConnection.connected is True:
           self.debug('frostbite2 server connected, removing crontab check_if_rcon_is_ready...')
           self.console.cron - self.wait_for_rcon_crontab # cancel the crontab job
           self.onRconReady()

    def apply_hardcore_settings(self):
        '''Applies all settings for a true hardcore server as stated in BF3 admin documentation'''
        try:
            self.debug('Loading Hardcore Settings...')
            self.console.setCvar('autoBalance', 'true')
            self.console.setCvar('friendlyFire', 'true')
            self.console.setCvar('killCam', 'false')
            self.console.setCvar('miniMap', 'true')
            self.console.setCvar('hud', 'false')
            self.console.setCvar('3dSpotting', 'false')
            self.console.setCvar('miniMapSpotting', 'true')
            self.console.setCvar('nameTag', 'false')
            self.console.setCvar('3pCam', 'false')
            self.console.setCvar('regenerateHealth', 'false')
            self.console.setCvar('vehicleSpawnAllowed', 'true')
            self.console.setCvar('soldierHealth', '60')
            self.console.setCvar('playerRespawnTime', '100')
            self.console.setCvar('playerManDownTime', '100')
            self.console.setCvar('bulletDamage', '100')
            self.console.setCvar('onlySquadLeaderSpawn', 'true')
            self.debug('Hardcore settings loaded successfully')
        except CommandFailedError, err:
            self.debug(err)
