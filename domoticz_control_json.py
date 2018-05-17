from __future__ import print_function

import requests
import json
import os, sys, time
import threading
#import subprocess, os, jsonrpclib, json, re, threading, time, traceback,sys

"""
This Library/Class is inspired by the description of the different JSON commands on:
https://www.domoticz.com/wiki/Domoticz_API/JSON_URL%27s

"""

def find_dict(list, key, value, returnIdx=False):
	for i, dic in enumerate(list):
		if dic[key] == value:
			if returnIdx:
				return i
			else:
				return dic
	return None
	
class DomoticzJSON():
	def __init__(self,IP="localhost",port=8080):
		self.apiUrl = "http://{}:{}/json.htm".format(IP,port)
		self.headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
		self.debug_level = 1
		self.devices = []

	def SwitchLight(self,idx,state="On",repeat=0):
		# http://192.168.11.4:8080/json.htm?type=command&param=switchlight&idx=41&switchcmd=On
		postdata = {'type':'command', 'param':'switchlight','idx':str(idx),'switchcmd':state}
		if self.debug_level == 1:
			print(postdata)
		for i in range(0,repeat+1):
			#response = requests.post(url,data=json.dumps(postdata),headers=self.headers)
			response = requests.get(url=self.apiUrl, params=postdata,headers=self.headers)
			if response.status_code != 200 and self.debug_level == 2:
				print(response.json())

	def SetColBrightnessValue(self,idx,int=100,hue=None,RGB_hex=None,color=None,iswhite="false",repeat=0):
		#http://192.168.11.4:8080/json.htm?type=command&param=setcolbrightnessvalue&idx=20&hue=274&brightness=40&iswhite=false
		#http://192.168.11.4:8080/json.htm?type=command&param=setcolbrightnessvalue&idx=20&hex=0000FF&brightness=100&iswhite=false
		#http://192.168.11.4:8080/json.htm?type=command&param=setcolbrightnessvalue&idx=20&color={"m":2,"t":127,"r":0,"g":0,"b":0,"cw":0,"ww":0}&brightness=40&iswhite=false
		#color_set = {"m":2,"t":127,"r":0,"g":0,"b":0,"cw":0,"ww":0}
		
		#ToDo: check that only one of the color parameters is filled, otherwise give warning
		postdata = {'type':'command', 'param':'setcolbrightnessvalue','idx':str(idx),'brightness':int}
		if hue != None:
			postdata['hue'] = hue
			postdata['iswhite'] = iswhite
		elif RGB_hex != None:
			postdata['hex'] = RGB_hex
			postdata['iswhite'] = iswhite
		elif color != None:
			postdata['color'] = color
			
		if self.debug_level == 1:
			print(postdata)
		for i in range(0,repeat+1):
			#response = requests.post(url,data=json.dumps(postdata),headers=self.headers)
			response = requests.get(url=self.apiUrl, params=postdata,headers=self.headers)
			if response.status_code  != 200 and self.debug_level == 2:
				print(response.json())

	def SetKelvinLevel(self,idx,cct=100,repeat=0):
		#http://192.168.11.4:8080/json.htm?type=command&param=setkelvinlevel&idx=20&kelvin=95
		postdata = {'type':'command', 'param':'setkelvinlevel','idx':str(idx),'kelvin':str(cct)}
		if self.debug_level == 1:
			print(postdata)
		for i in range(0,repeat+1):
			#response = requests.post(url,data=json.dumps(postdata),headers=self.headers)
			response = requests.get(url=self.apiUrl, params=postdata,headers=self.headers)
			if response.status_code  != 200 and self.debug_level == 2:
				print(response.json())


	def GetDeviceList(self):
		#http://192.168.11.4:8080/json.htm?type=devices&filter=light&used=true&order=Name
		#check that only one of the color parameters is filled, otherwise give warning
		postdata = {'type':'devices', 'filter':'all','used':'true','order':'Name'}
		#light = Get all lights/switches
		#weather = Get all weather devices
		#temp = Get all temperature devices
		#utility = Get all utility devices
		if self.debug_level == 1:
			print(postdata)
		response = requests.get(url=self.apiUrl, params=postdata,headers=self.headers)
		resp_json = response.json()
		if response.status_code  != 200 and self.debug_level == 2:
			print(resp_json)
		if 'result' in resp_json:
			self.devices = resp_json['result']
			if self.debug_level == 1:
				print("Lights/Switches:\n{}".format(json.dumps(self.devices, indent=4, sort_keys=False)))
			
"""
class WebSocketWorkerThread(threading.Thread):

	def __on_message(self, ws, message):
		try:
			print("message:"+str(message))
			#json_message = json.loads(message)

		except Exception as exc:
			print("Unrecognized message received: ")
			print(message)
			print(exc)

	def __on_error(self, ws, error):
		print("error:"+str(error))

	def __on_close(self, ws):
		print("### websocket closed ###")

	def __on_open(self, ws):
		print('### websocket opened ###')

	def __init__(self,IP="localhost",port=8080,verbose=False):
		threading.Thread.__init__(self)
		self.apiUrl = "wss://{}:{}/json.htm".format(IP,port)

		websocket.enableTrace(verbose)
		self.ws = websocket.WebSocketApp(self.apiUrl,
						  on_message = self.__on_message,
						  on_error = self.__on_error,
						  on_close = self.__on_close)
		self.ws.on_open = self.__on_open

	def run(self):
		self.ws.run_forever()

	def close_websocket(self):
		self.ws.close()

	def send_json_msg(self, msg):
		# see __init__ to enable verbose output
		self.ws.send(json.dumps(msg))
"""

domjson = DomoticzJSON("192.168.11.4",8080)
domjson.GetDeviceList()

TV_SW = find_dict(domjson.devices, 'Name', "TV_SW", returnIdx=False)
Vitr_SW = find_dict(domjson.devices, 'Name', "Vitrine_SW", returnIdx=False)

TV_RGBCCT = find_dict(domjson.devices, 'Name', "TV_RGBCCT01", returnIdx=False)
TV_CCT = find_dict(domjson.devices, 'Name', "TV_CCT01", returnIdx=False)
Vitr_RGBW = find_dict(domjson.devices, 'Name', "Vitrine_RGBW04", returnIdx=False)
OVR_RGBW = find_dict(domjson.devices, 'Name', "OVR_RGBW_02", returnIdx=False)

domjson.SwitchLight(TV_SW["idx"],state="On",repeat=3)
time.sleep(1)
domjson.SwitchLight(Vitr_SW["idx"],state="On",repeat=3)
time.sleep(1)

domjson.SetColBrightnessValue(Vitr_RGBW["idx"],int=100,RGB_hex="007F7F",repeat=2)
time.sleep(1)

for i in range(0,20):
	domjson.SetKelvinLevel(TV_CCT["idx"],cct=str(i*5),repeat=0)

domjson.SetColBrightnessValue(TV_RGBCCT["idx"],int=100,RGB_hex="7F0000",repeat=2)
for i in range(0,36):
	domjson.SetColBrightnessValue(TV_RGBCCT["idx"],int=100,hue=str(i*10),repeat=0)
	#domjson.SetColBrightnessValue(20,int=100,RGB_hex="0000FF",repeat=2)

time.sleep(1)

domjson.SwitchLight(TV_SW["idx"],state="Off",repeat=3)
time.sleep(1)
domjson.SwitchLight(Vitr_SW["idx"],state="Off",repeat=3)
time.sleep(1)

sys.exit()

#ft_server_ip = os.environ.get('FTS_IP', "localhost")
server_ip = "192.168.11.4"
#server_ip = "192.168.11.4"
server_port = 8080
url = "http://{}:{}/json.htm".format(server_ip,server_port)
headers = {'content-type':'application/json'}
#http://192.168.11.4:8080/json.htm?type=command&param=switchlight&idx=41&switchcmd=On
#response = curl 'http://{}:{}/json.htm?type=command&param=switchlight&idx={}&switchcmd={}'.format(server_ip,server_port,41,"On")

#TV
postdata = {'type':'command', 'param':'switchlight','idx':'39','switchcmd':'On'}
print(postdata)
#response = requests.post(url,data=json.dumps(postdata),headers =headers)
response = requests.get(url=url, params=postdata,headers =headers)
response = requests.get(url=url, params=postdata,headers =headers)
print(response)
print(requests.post)
time.sleep(1)
# Vitrine
postdata['idx'] = '41'
response = requests.get(url=url, params=postdata,headers =headers)
response = requests.get(url=url, params=postdata,headers =headers)
print(response)

time.sleep(1)
"""
ColorMode {
	ColorModeNone = 0,   // Illegal
	ColorModeWhite = 1,  // White. Valid fields: none
	ColorModeTemp = 2,   // White with color temperature. Valid fields: t
	ColorModeRGB = 3,    // Color. Valid fields: r, g, b.
	ColorModeCustom = 4, // Custom (color + white). Valid fields: r, g, b, cw, ww, depending on device capabilities
	ColorModeLast = ColorModeCustom,
};

Color {
	ColorMode m;
	uint8_t t;     // Range:0..255, Color temperature (warm / cold ratio, 0 is coldest, 255 is warmest)
	uint8_t r;     // Range:0..255, Red level
	uint8_t g;     // Range:0..255, Green level
	uint8_t b;     // Range:0..255, Blue level
	uint8_t cw;    // Range:0..255, Cold white level
	uint8_t ww;    // Range:0..255, Warm white level (also used as level for monochrome white)
}
"""
#/json.htm?type=command&param=setcolbrightnessvalue&idx=130&color={"m":3,"t":0,"r":0,"g":0,"b":50,"cw":0,"ww":0}&brightness=100
color_set = {"m":2,"t":127,"r":0,"g":0,"b":0,"cw":0,"ww":0}
postdata = {'type':'command', 'param':'setcolbrightnessvalue','idx':'20','color':color_set,'brightness':100}

"""
http://192.168.11.4:8080/json.htm?type=command&param=setcolbrightnessvalue&idx=20&hue=274&brightness=40&iswhite=false
http://192.168.11.4:8080/json.htm?type=command&param=setcolbrightnessvalue&idx=20&hex=0000FF&brightness=100&iswhite=false

Milight supports 256 colors 00-FF there is no specific RGB value
The brightness is controlled in 32 steps. 

In the hardware tab, select the "Create RFLink Devices" button and in the popup enter:
10;rfdebug=on;
to activate the debug feature within the Domoticz log.
and
10;rfdebug=off;
to deactivate the debug feature. 
"""
print(postdata)
response = requests.get(url=url, params=postdata,headers =headers)
print(response)
time.sleep(1)


#TV
postdata = {'type':'command', 'param':'switchlight','idx':'39','switchcmd':'On'}
postdata['switchcmd'] = 'Off'
postdata['idx'] = '39'
response = requests.get(url=url, params=postdata,headers =headers)
response = requests.get(url=url, params=postdata,headers =headers)
print(response)

time.sleep(1)
#Vitrine
postdata['idx'] = '41'
response = requests.get(url=url, params=postdata,headers =headers)
response = requests.get(url=url, params=postdata,headers =headers)
print(response)


