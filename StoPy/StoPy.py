#!/usr/local/bin/python
import requests
import json
from urlparse import urlparse

class StoPy:
#constructor
	def __init__(self, server, api_key, port=False, protocol="https", version = "v1"):
		self.server = server
		self.port = port
		self.api_key = api_key
		self.headers = self.createHeaders( self.api_key )
		self.protocol = protocol
		serverParse = urlparse( server )
		if serverParse.scheme != '':
			self.protocol = serverParse.scheme
		if serverParse.port != '' and str(serverParse.port) != 'None' and port == False:
			self.port = serverParse.port
		if self.port == False and self.protocol == "https":
			self.port = 443
		if self.port == False and self.protocol == "http":
			self.port = 80
		self.connected = False
		while self.connected != True:
			try:
				self.uri = str(self.protocol) + "://" + str(self.server) + ":" + str(self.port) + "/"
				r = requests.get(url = self.uri, headers = self.headers )
				if r.status_code != 200:
					print( self.handleError( "Error connecting to " + str( self.uri ) ) )
					quit()
				else:
					self.connected = True
					validateKey = self.uri + "/validateKey"
					r2 = requests.get(url = validateKey, headers = self.headers )
					if r2.status_code != 200:
						print( self.handleError( "Error validating API Key" ) )
						quit()
			except:
				print( self.handleError( "Error connecting to " + str( self.uri ) ) )
				if self.protocol == "https":
					print( "Falling back to http" )
					self.protocol = "http"
					if self.port == 443:
						self.port = 80
				else:
					quit()

		self.uri = self.uri + str( version )

#create functionality
	#save data
	def insert(self, collection, owner, content, api_key=False):
		headers = self.customHeaders( api_key )
		uri = self.uri + "/insert"
		data = { 'data': content ,'owner': owner }
		if collection != False:
			data['collection'] = collection
		try:
			r = requests.post( url=uri, headers=headers, json=data )
			return json.loads(r.text)
		except:
			return self.handleError("Error Inserting")

	def updateId(self, collection, _id, content, api_key=False):
		headers = self.customHeaders( api_key )
		uri = self.uri + "/update"
		data = { 'data': content ,'id': _id }
		if collection != False:
			data['collection'] = collection
		try:
			r = requests.put( url=uri, headers=headers, json=data )
			return json.loads(r.text)
		except:
			return self.handleError("Error Updating")

	def updateOwner(self, collection, new_owner, old_owner, api_key=False):
		headers = self.customHeaders( api_key )
		uri = self.uri + "/update"
		data = { 'new_owner': new_owner, 'old_owner': old_owner }
		if collection != False:
			data['collection'] = collection
		try:
			r = requests.put( url=uri, headers=headers, json=data )
			return json.loads(r.text)
		except:
			return self.handleError("Error Updating")

#read functionality	
	#read data by id
	def readLatest(self, collection, id, api_key=False ):
		headers = self.customHeaders( api_key )
		uri = self.uri + ( "/" + str(collection) if collection != False else "" ) + "/id/" + str(id) + "/"
		return self.getData(uri, headers, "Error Fetching Last Data")

	#read data descending
	def readLatest(self, collection, owner, limit=False, api_key=False ):
		headers = self.customHeaders( api_key )
		uri = self.uri + ( "/" + str(collection) if collection != False else "" ) + "/last/" + str(owner) + "/"
		if limit != False:
			uri = uri + str(limit)
		return self.getData(uri, headers, "Error Fetching Last Data")

	#read data descending -- paginated
	def readLatestByPage(self, collection, owner, items_per_page=1, page_number=0, api_key=False ):
		headers = self.customHeaders( api_key )
		uri = self.uri + ( "/" + str(collection) if collection != False else "" ) + "/last/" + str(owner) + "/" + str(items_per_page) + "/page/" + str(page_number)
		return self.getData(uri, headers, "Error Fetching Page Data" )

	#read data ascending
	def readOldest(self, collection, owner, limit=False, api_key=False ):
		headers = self.customHeaders( api_key )
		uri = self.uri + ( "/" + str(collection) if collection != False else "" ) + "/first/" + str(owner) + "/"
		if limit != False:
			uri = uri + str(limit)
		return self.getData(uri, headers,  "Error Fetching Last Data" )

	#read data ascending -- paginated
	def readOldestByPage(self, collection, owner, items_per_page=1, page_number=0, api_key=False ):
		headers = self.customHeaders( api_key )
		uri = self.uri + ( "/" + str(collection) if collection != False else "" ) + "/first/" + str(owner) + "/" + str(items_per_page) + "/page/" + str(page_number)
		print( uri )
		return self.getData(uri, headers,  "Error Fetching Page Data" )

	#read data using hashData
	def readHash(self, collection, hashData, owner=False, api_key=False ):
		headers = self.customHeaders( api_key )
		uri = self.uri + ( "/" + str(collection) if collection != False else "" ) + "/hash/" + str(hashData) + "/"
		if owner != False:
			uri = uri + owner + "/"
		return self.getData(uri, headers, "Error Fetching Hash Data" )

	#read id using hashData
	def readId(self, collection, _id, api_key=False ):
		headers = self.customHeaders( api_key )
		uri = self.uri + ( "/" + str(collection) if collection != False else "" ) + "/id/" + str(_id) + "/"
		return self.getData(uri, headers, "Error Fetching Hash Data" )

	#read total count of collection (by owner)
	def getCount(self, collection, owner=False, api_key=False):
		headers = self.customHeaders( api_key )
		uri = self.uri + ( "/" + str(collection) if collection != False else "" ) + "/count/"
		if owner != False: 
			uri = uri + str(owner) + "/"
		return self.getData(uri, headers, "Error Fetching Count" )

#delete functionality
	#delete individual data by id
	def deleteById(self, collection, id, api_key=False):
		headers = self.customHeaders( api_key )
		uri = self.uri + "/delete"
		data = { 'id': id }
		if collection != False:
			data['collection'] = collection
		try:
			r = requests.delete( url=uri, headers=headers, json=data )
			return json.loads(r.text)
		except:
			return self.handleError("Error Deleting")

	#delete individual data by hash
	def deleteByHash(self, collection, hashData, owner=False, api_key=False):
		headers = self.customHeaders( api_key )
		uri = self.uri + "/delete"
		data = { 'hashData': hashData }
		if collection != False:
			data['collection'] = collection
		if owner != False:
			data['owner'] = owner
		try:
			r = requests.delete( url=uri, headers=headers, json=data )
			return json.loads(r.text)
		except:
			return self.handleError("Error Deleting")

	#delete all data by owner (save is a count of saved data)
	def deleteByOwner(self, collection, owner, save = False, api_key = False):
		headers = self.customHeaders( api_key )
		uri = self.uri + "/delete"
		data = { 'owner': owner }
		if collection != False:
			data['collection'] = collection
		if save != False and int(save) > 0:
			data['skip'] = int(save)
		try:
			r = requests.delete( url=uri, headers=headers, json=data )
			return json.loads(r.text)
		except:
			return self.handleError("Error Deleting")

#helpers
	#overwrite system headers
	def customHeaders(self, api_key=False ):
		if( api_key != False ):
			return self.createHeaders( api_key )
		else:
			return self.headers

	#standard format for request headers
	def createHeaders(self, api_key ):
		return {
			'Content-Type': 'application/json',
			'authorization': 'Basic api_key='+str(api_key)
		}

	#generic error handler
	def handleError(self, error ):
		return { 'errors': [ "[CLIENT] " + str(error) ] }

	#generic get request format
	def getData(self, uri, headers, error):
		try:
			r = requests.get( url=uri, headers=headers )
			return json.loads(r.text)
		except:
			return self.handleError( error )
