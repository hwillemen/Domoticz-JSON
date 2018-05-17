from __future__ import print_function

import requests
import json
import os, time
#import subprocess, os, jsonrpclib, json, re, threading, time, traceback,sys


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

	def SwitchLight(self,idx,state="On",repeat=0):


setcolbrightnessvalue


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
		#self.handlers = FunctionHandlers(device_mesh)

	def run(self):
		self.ws.run_forever()

	def close_websocket(self):
		self.ws.close()

	def send_json_msg(self, msg):
		# see __init__ to enable verbose output
		self.ws.send(json.dumps(msg))
"""


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


