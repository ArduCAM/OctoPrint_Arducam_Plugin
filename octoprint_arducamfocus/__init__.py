# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

from __future__ import absolute_import
from octoprint.access.permissions import Permissions, ADMIN_GROUP
import octoprint.plugin
import flask,json
from octoprint.server.util.flask import restricted_access
import smbus
import os
import time
import sys
import subprocess

class ArducamfocusPlugin(octoprint.plugin.SettingsPlugin,
							octoprint.plugin.TemplatePlugin,
							octoprint.plugin.AssetPlugin,
							octoprint.plugin.StartupPlugin,
							octoprint.plugin.BlueprintPlugin,
							octoprint.plugin.EventHandlerPlugin,
							octoprint.plugin.SimpleApiPlugin,
							octoprint.plugin.OctoPrintPlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
			available="[]"
		)

	##~~ AssetPlugin mixin

	def on_after_startup(self):
		ID = self.inquire()
		if ID=='0':
			ID='10'
		else:
			ID='1'
		self.bus = smbus.SMBus(int(ID))
		self.getAddresses()
		self.time = time.time()

	def getAddresses(self):
		availableArray=[]
		n=1
		while n<128:
			if n<0x10:
				available=os.popen('i2cdetect -y 1 | grep 0'+hex(n))
			else:
				available=os.popen('i2cdetect -y 1 | grep '+hex(n))
			if available != "":
				availableArray.append(n)
			n+=1
		self._settings.set(["available"],json.dumps(availableArray))
		self._settings.save()

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/arducamfocus.js"],
			css=["css/arducamfocus.css"],
			less=["less/arducamfocus.less"]
		)

	##~~ Access Permissions Hook
	def get_permissions(self, *args, **kwargs):
		return [
			dict(key="ADMIN",
				 name="Admin",
				 description="Access to control of robot",
				 roles=["admin"],
				 dangerous=True,
				 default_groups=[ADMIN_GROUP])
		]
	##~~ Softwareupdate hook

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			arducamfocus=dict(
				displayName="Arducamfocus Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="you",
				repo="OctoPrint-Arducamfocus",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/you/OctoPrint-Arducamfocus/archive/{target_version}.zip"
			)
		)


	def focus (self, f): 
		if f < 100:
			f = 100
		elif f > 1000:
			f = 1000
		value = (f << 4) & 0x3ff0
		data1 = (value >> 8) & 0x3f
		data2 = value & 0xf0
		if self.bus:
			write_attempts = 10
			while write_attempts:
				try:
					self.bus.write_byte_data(0xc, data1, data2)
				except IOError:
					write_attempts -= 1
				else:
					break
			if not write_attempts:
				self._plugin_manager.send_plugin_message(self._identifier, dict(error="Trouble accessing camera. I2C bus failure.  Is camera plugged in?"))
		else:
			self._plugin_manager.send_plugin_message(self._identifier, dict(error="unable to use SMBus/I2C"))


	def ptz_zoom (self, f): 
		databuf=[0xff,0xff]
		databuf[0]=(f>>8)&0xff
		databuf[1]=f&0xff 
		state=self.bus.read_i2c_block_data(0x0c,0x04,2)
		if (state[1]&0x01)==0:
			if self.bus:
				write_attempts = 10
				while write_attempts:
					try:
						self.bus.write_i2c_block_data(0xc,0x00, databuf)
					except IOError:
						write_attempts -= 1
					else:
						break
				if not write_attempts:
					self._plugin_manager.send_plugin_message(self._identifier, dict(error="Trouble accessing camera. I2C bus failure.  Is camera plugged in?"))
			else:
				self._plugin_manager.send_plugin_message(self._identifier, dict(error="unable to use SMBus/I2C"))	


	def ptz_focus (self, f): 
		if tmp=='1':
			databuf=[0xff,0xff]
			databuf[0]=(f>>8)&0xff
			databuf[1]=f&0xff
			state=self.bus.read_i2c_block_data(0x0c,0x04,2)
			if (state[1]&0x01)==0:
				if self.bus:
					write_attempts = 10
					while write_attempts:
						try:
							self.bus.write_i2c_block_data(0xc,0x01, databuf)
						except IOError:
							write_attempts -= 1
						else:
							break
					if not write_attempts:
						self._plugin_manager.send_plugin_message(self._identifier, dict(error="Trouble accessing camera. I2C bus failure.  Is camera plugged in?"))
				else:
					self._plugin_manager.send_plugin_message(self._identifier, dict(error="unable to use SMBus/I2C"))	
		elif tmp=='0':
			if f < 100:
				f = 100
			elif f > 1000:
				f = 1000
			value = (f << 4) & 0x3ff0
			data1 = (value >> 8) & 0x3f
			data2 = value & 0xf0
			if self.bus:
				write_attempts = 10
				while write_attempts:
					try:
						self.bus.write_byte_data(0xc, data1, data2)
					except IOError:
						write_attempts -= 1
					else:
						break
				if not write_attempts:
					self._plugin_manager.send_plugin_message(self._identifier, dict(error="Trouble accessing camera. I2C bus failure.  Is camera plugged in?"))
			else:
				self._plugin_manager.send_plugin_message(self._identifier, dict(error="unable to use SMBus/I2C"))
	def ptz_pan (self, f): 
		databuf=[0xff,0xff]
		databuf[0]=(f>>8)&0xff
		databuf[1]=f&0xff
		if self.bus:
			write_attempts = 10
			while write_attempts:
				try:
					self.bus.write_i2c_block_data(0xc,0x05, databuf)
				except IOError:
					write_attempts -= 1
				else:
					break
			if not write_attempts:
				self._plugin_manager.send_plugin_message(self._identifier, dict(error="Trouble accessing camera. I2C bus failure.  Is camera plugged in?"))
		else:
			self._plugin_manager.send_plugin_message(self._identifier, dict(error="unable to use SMBus/I2C"))	

	def ptz_til (self, f): 
		databuf=[0xff,0xff]
		databuf[0]=(f>>8)&0xff
		databuf[1]=f&0xff
		if self.bus:
			write_attempts = 10
			while write_attempts:
				try:
					self.bus.write_i2c_block_data(0xc,0x06, databuf)
				except IOError:
					write_attempts -= 1
				else:
					break
			if not write_attempts:
				self._plugin_manager.send_plugin_message(self._identifier, dict(error="Trouble accessing camera. I2C bus failure.  Is camera plugged in?"))
		else:
			self._plugin_manager.send_plugin_message(self._identifier, dict(error="unable to use SMBus/I2C"))	

	def ptz_ircut (self, f): 
		databuf=[0xff,0xff]
		databuf[0]=(f>>8)&0xff
		databuf[1]=f&0xff
		if self.bus:
			write_attempts = 10
			while write_attempts:
				try:
					self.bus.write_i2c_block_data(0xc,0x0c, databuf)
				except IOError:
					write_attempts -= 1
				else:
					break
			if not write_attempts:
				self._plugin_manager.send_plugin_message(self._identifier, dict(error="Trouble accessing camera. I2C bus failure.  Is camera plugged in?"))
		else:
			self._plugin_manager.send_plugin_message(self._identifier, dict(error="unable to use SMBus/I2C"))		
	
	def inquire(self):
		cmd = "find /dev/i2c* | awk -F '-' '{print $NF}'"
		IP = subprocess.check_output(cmd, shell=True).decode('utf-8')
		IP=IP.split('\n')
		i2c0flag=0
		i2c1flag=0
		for num in IP:
			if num in ['0','1','10']:
				cmd = "i2cdetect -y %s | awk 'NR==2 {print $11}'" % num
				data = subprocess.check_output(cmd, shell=True).decode('utf-8')
				if data=="0c\n":
					if num=='1':
						return num
					else:
						return '0'
		if i2c0flag==0 and i2c1flag==0:
			return '2'

	# @octoprint.plugin.BlueprintPlugin.route("/focus", methods=["GET"])
	# @restricted_access
	# def setAngle1(self):
	# 	if not Permissions.PLUGIN_ARDUCAMFOCUS_ADMIN.can():
	# 		return flask.make_response("403 Failure. Check that you are an admin", 403)
	# 	if time.time()-self.time>0.1:
	# 		self.time=time.time()
	# 		angle = int(flask.request.args.get("value", 0))
	# 		#angle is an integer from 0 to 180
	# 		self.focus(angle)
	# 	return flask.make_response("Too Fast!", 200)

	@octoprint.plugin.BlueprintPlugin.route("/ptz_inquire", methods=["GET"])
	@restricted_access
	def setptzinquire(self):
		if not Permissions.PLUGIN_ARDUCAMFOCUS_ADMIN.can():
			return flask.make_response("403 Failure. Check that you are an admin", 403)
		if time.time()-self.time>0.1:
			self.time=time.time()
			angle = int(flask.request.args.get("value", 0))
			# angle is an integer from 0 to 180
			global tmp
			tmp = self.inquire()
			return flask.make_response(tmp, 200)
		return flask.make_response("Too Fast!", 200)


	@octoprint.plugin.BlueprintPlugin.route("/ptz_zoom", methods=["GET"])
	@restricted_access
	def setptzzoom(self):
		if not Permissions.PLUGIN_ARDUCAMFOCUS_ADMIN.can():
			return flask.make_response("403 Failure. Check that you are an admin", 403)
		if time.time()-self.time>0.1:
			self.time=time.time()
			angle = int(flask.request.args.get("value", 0))
			#angle is an integer from 0 to 180
			self.ptz_zoom(angle)
			return flask.make_response("success", 200)
		return flask.make_response("Too Fast!", 200)

	@octoprint.plugin.BlueprintPlugin.route("/ptz_focus", methods=["GET"])
	@restricted_access	
	def setptzfocus(self):
		if not Permissions.PLUGIN_ARDUCAMFOCUS_ADMIN.can():
			return flask.make_response("403 Failure. Check that you are an admin", 403)
		if time.time()-self.time>0.1:
			self.time=time.time()
			angle = int(flask.request.args.get("value", 0))
			#angle is an integer from 0 to 180
			self.ptz_focus(angle)
			return flask.make_response("success ", 200)
		return flask.make_response("Too Fast!", 200)

	@octoprint.plugin.BlueprintPlugin.route("/ptz_pan", methods=["GET"])
	@restricted_access	
	def setptzpan(self):
		if not Permissions.PLUGIN_ARDUCAMFOCUS_ADMIN.can():
			return flask.make_response("403 Failure. Check that you are an admin", 403)
		if time.time()-self.time>0.1:
			self.time=time.time()
			angle = int(flask.request.args.get("value", 0))
			#angle is an integer from 0 to 180
			self.ptz_pan(180-angle)
			return flask.make_response("success", 200)
		return flask.make_response("Too Fast!", 200)

	@octoprint.plugin.BlueprintPlugin.route("/ptz_til", methods=["GET"])
	@restricted_access	
	def setptztil(self):
		if not Permissions.PLUGIN_ARDUCAMFOCUS_ADMIN.can():
			return flask.make_response("403 Failure. Check that you are an admin", 403)
		if time.time()-self.time>0.1:
			self.time=time.time()
			angle = int(flask.request.args.get("value", 0))
			#angle is an integer from 0 to 180
			self.ptz_til(angle)
			return flask.make_response("success", 200)
		return flask.make_response("Too Fast!", 200)
	
	@octoprint.plugin.BlueprintPlugin.route("/ptz_ircut", methods=["GET"])
	@restricted_access	
	def setptzircut(self):
		if not Permissions.PLUGIN_ARDUCAMFOCUS_ADMIN.can():
			return flask.make_response("403 Failure. Check that you are an admin", 403)
		if time.time()-self.time>0.1:
			self.time=time.time()
			angle = int(flask.request.args.get("value", 0))
			#angle is an integer from 0 to 180
			self.ptz_ircut(angle)
			return flask.make_response("success", 200)
			# self.focus(angle)
		return flask.make_response("Too Fast!", 200)

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Arducamfocus Plugin"
__plugin_pythoncompat__ = ">=2.7,<4"
# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ArducamfocusPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.access.permissions": __plugin_implementation__.get_permissions
	}

