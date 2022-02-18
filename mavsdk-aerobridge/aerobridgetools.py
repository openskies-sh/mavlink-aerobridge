import requests, json

# Version: 0.0.1

class AerobridgeClient():
	'''
	This a a Python client that make calls to the Aerobridge API
	and returns data. It requires the requests package and the json module. 

	'''

	def __init__(self, aerobridge_url, token, authority_url):
		'''
		Declare your Aerobridge instance, token and the url (optional). 
		'''		
		self.token = token
		self.aerobridge_url = aerobridge_url if aerobridge_url else 'https://aerobridgetestflight.herokuapp.com/api/v1/'		
		self.session = requests.Session()
		self.authority_url = authority_url
		
	def ping_aerobridge(self):
		''' This method pings and Aerobridge instance '''
		aerobridge_url = self.aerobridge_url+ 'ping/'
		headers = {'Authorization': 'Token '+ self.token}
		r = self.session.get(aerobridge_url, headers=headers)
		return r
        
	def get_authority_public_key(self):
		''' This method gets the public key from the token authority as JWKS '''
		raise NotImplementedError

	def download_flight_permission(self, operation_id):
		''' This method downloads flight permission object given a operation ''' 
		raise NotImplementedError

	def download_flight_plan(self, plan_id):
		''' This method downloads the flight plan in the form of a plan file given the flight plan id '''
		raise NotImplementedError

	def get_latest_firmware(self, firmware_id):
		''' This method downloads the latest firmware  in the form of a plan file given the flight plan id '''
		raise NotImplementedError

	def get_all_aircrafts(self):
		''' This method downloads all aircrafts in the management server '''
		raise NotImplementedError

	def get_aircraft_by_flight_controller_id(self, flight_controller_id):
		''' This method downloads all aircrafts in the management server '''
		raise NotImplementedError
		
	def get_firmware_by_flight_controller_id(self, flight_controller_id):
		''' This method downloads all aircrafts in the management server '''
		raise NotImplementedError