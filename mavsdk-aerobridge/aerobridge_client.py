import requests, json

# Version: 1.2.5

class AerobridgeClient():
	'''
	This a a Python client that make calls to the Aerobridge API
	and return data. It requires the requests package and the json module. 

	'''

	def __init__(self, url, token):
		'''
		Declare your Aerobridge instance, token and the url (optional). 
		'''		
		self.token = token
		self.securl = url if url else 'https://aerobridgetestflight.herokuapp.com/api/v1/'		
		self.session = requests.Session()

	def ping_aerobridge(self):
		''' This method pings and Aerobridge instance '''
		securl = self.securl+ 'ping/'
		headers = {'Authorization': 'Token '+ self.token}
		r = self.session.get(securl, headers=headers)
		return r
        