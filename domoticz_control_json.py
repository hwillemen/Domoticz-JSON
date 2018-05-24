#!/usr/bin/python
from __future__ import print_function

try:
	import DomoticzEvents as DE
	ScriptRunExternal = False
except:
	ScriptRunExternal = True
	
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

def filter_dicts(list, key, str, search="contains"):
	return_list = []
	for i, dic in enumerate(list):
		if search == "endswith" and dic[key].endswith(str):
			return_list.add(dic)
		elif search == "startswith" and dic[key].startswith(str):
			return_list.add(dic)
		elif search == "contains" and dic[key].find(str):
			return_list.add(dic)				
	return return_list
	
class DomoticzJSON():
	def __init__(self,IP="localhost",port=8080):
		self.apiUrl = "http://{}:{}/json.htm".format(IP,port)
		self.headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
		self.debug_level = 1
		self.devices = []

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

	def SwitchLight(self,idx,state="On",repeat=0):
		# http://192.168.11.4:8080/json.htm?type=command&param=switchlight&idx=41&switchcmd=On
		postdata = {'type':'command', 'param':'switchlight','idx':str(idx),'switchcmd':state}
		if self.debug_level == 1:
			print(postdata)
		for i in range(0,repeat+1):
			#response = requests.post(url,data=json.dumps(postdata),headers=self.headers)
			response = requests.get(url=self.apiUrl, params=postdata,headers=self.headers)
			if response.status_code != 200 or self.debug_level == 2:
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
			if response.status_code  != 200 or self.debug_level == 2:
				print(response.json())
	
	def SetKelvinLevel(self,idx,cct=100,repeat=0):
		#http://192.168.11.4:8080/json.htm?type=command&param=setkelvinlevel&idx=20&kelvin=95
		postdata = {'type':'command', 'param':'setkelvinlevel','idx':str(idx),'kelvin':str(cct)}
		if self.debug_level == 1:
			print(postdata)
		for i in range(0,repeat+1):
			#response = requests.post(url,data=json.dumps(postdata),headers=self.headers)
			response = requests.get(url=self.apiUrl, params=postdata,headers=self.headers)
			if response.status_code  != 200 or self.debug_level == 2:
				print(response.json())


	def GetSensorData(self,name=None,idx=None,filter='temp'):
		# there is no json command to read sensor information, but we can filter it from the device list
		if name == None and idx == None:
			print("GetSensorData requires a name or an idx")
			return None
			
		if filter == 'temp' or filter == 'weather':
			relevant_keys = ["idx","Type","Temp","Barometer","Humidity","DewPoint","HumidityStatus","ForecastStr"]		
		elif filter == 'utility':
			relevant_keys = ["idx","Type"]		

		# get current state of sensor devices:
		postdata = {'type':'devices', 'filter':filter,'used':'true','order':'Name'}
		response = requests.get(url=self.apiUrl, params=postdata,headers=self.headers)
		resp_json = response.json()
		if response.status_code  != 200 or self.debug_level == 2:
			print(resp_json)
		if 'result' in resp_json:
			if idx != None: #get sensor by idx
				device = find_dict(resp_json['result'], 'idx', str(idx), returnIdx=False)
			elif name != None: #get sensor by name
				device = find_dict(resp_json['result'], 'Name', name, returnIdx=False)
			if self.debug_level == 2:
				print(device)
			print(device)
			#copy relevant info to return_dict
			#used dictionary comprehension: https://stackoverflow.com/questions/1747817/create-a-dictionary-with-list-comprehension-in-python
			return_dict = {key: value for (key, value) in device.items() if (key in relevant_keys)}
			if self.debug_level == 1:
				print("sensor data:\n{}".format(json.dumps(return_dict, indent=4, sort_keys=False)))
			return return_dict
			
	
domjson = DomoticzJSON("192.168.11.4",8080)
domjson.GetDeviceList()

if ScriptRunExternal:
	print("control script run external")
else:
	DE.Log("Script runs internal in Domoticz")
	
THB = domjson.GetSensorData(name="THB",filter='temp')
TV_SW = find_dict(domjson.devices, 'Name', "TV_SW", returnIdx=False)
Vitr_SW = find_dict(domjson.devices, 'Name', "Vitrine_SW", returnIdx=False)

TV_RGBCCT = find_dict(domjson.devices, 'Name', "TV_RGBCCT01", returnIdx=False)
TV_CCT = find_dict(domjson.devices, 'Name', "TV_CCT01", returnIdx=False)
Vitr_RGBW = find_dict(domjson.devices, 'Name', "Vitrine_RGBW04", returnIdx=False)
OVR_RGBW = find_dict(domjson.devices, 'Name', "OVR_RGBW02", returnIdx=False)

domjson.SwitchLight(TV_SW["idx"],state="On",repeat=3)
time.sleep(1)
domjson.SwitchLight(Vitr_SW["idx"],state="On",repeat=3)
time.sleep(1)

domjson.SetColBrightnessValue(Vitr_RGBW["idx"],int=100,RGB_hex="007F7F",repeat=2)
time.sleep(1)

for i in range(0,20):
	domjson.SetKelvinLevel(TV_CCT["idx"],cct=str(i*5),repeat=0)

domjson.SetColBrightnessValue(TV_RGBCCT["idx"],int=100,RGB_hex="007F7F",repeat=2)
for i in range(0,36):
	domjson.SetColBrightnessValue(OVR_RGBW["idx"],int=100,hue=str(i*10),repeat=0)
	#domjson.SetColBrightnessValue(20,int=100,RGB_hex="0000FF",repeat=2)

time.sleep(1)

domjson.SwitchLight(TV_SW["idx"],state="Off",repeat=3)
time.sleep(1)
domjson.SwitchLight(Vitr_SW["idx"],state="Off",repeat=3)
time.sleep(1)

sys.exit()