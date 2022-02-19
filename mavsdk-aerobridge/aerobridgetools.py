import requests
from uuid import UUID
# Version: 0.0.1

class AuthorityCredentialsGetter():
	''' All calls to the Aerobridge requires credentials from a oauth server, in this case this is Flight Passport  '''
	def __init__(self, client_id:str, client_secret:str, audience:str, base_url:str, token_endpoint:str, jwks_endpoint:str):

		self.client_id = client_id
		self.client_secret = client_secret
		self.audience = audience
		self.base_url = base_url
		self.token_url = base_url + token_endpoint		
		self.jwks_url = base_url + jwks_endpoint

	def get_credentials(self):  
		''' 
		Get client credentials 
		'''
		payload = {"grant_type":"client_credentials","client_id": self.client_id,"client_secret": self.client_secret,"audience": self.audience,"scope": 'aerobridge.read aerobridge.write'}          
		url = self.token_url
		
		token_data = requests.post(url, data = payload)
		t_data = token_data.json()     
		return t_data
		
	def get_public_key(self):  
		'''
		A class to get public key from the OAUTH server
		'''		
		url = self.jwks_url		
		jwks_data = requests.get(url)
		jwks_data = jwks_data.json()     
		return jwks_data

class AerobridgeClient():
	'''
	This a a Python client that make calls to the Aerobridge API
	and returns data. It requires the requests package and the json module. 

	'''

	def __init__(self, aerobridge_url:str, token, authority_url:str):
		'''
		Declare your Aerobridge instance, token and the url (optional). 
		'''		
		self.token = token
		self.aerobridge_url = aerobridge_url if aerobridge_url else 'https://aerobridgetestflight.herokuapp.com/'		
		self.session = requests.Session()
		self.authority_url = authority_url
		
	def ping_aerobridge(self):
		''' This method pings and Aerobridge instance '''
		aerobridge_url = self.aerobridge_url+ 'ping/'
		headers = {'Authorization': 'Bearer '+ self.token}
		r = self.session.get(aerobridge_url, headers=headers)
		return r
        
	def download_flight_permission(self, operation_id:UUID):
		''' This method downloads flight permission object given a operation ''' 
		securl = self.aerobridge_url + 'gcs/flight-operations/' + operation_id + '/permission'
		headers = {'Authorization': 'Bearer '+ self.token}
		r = self.session.put(securl, headers= headers)
		return r

	def download_flight_plan(self, plan_id):
		''' This method downloads the flight plan in the form of a plan file given the flight plan id '''
		securl = self.aerobridge_url + 'gcs/flight-plans/' + plan_id
		headers = {'Authorization': 'Bearer '+ self.token, 'content-type': 'application/json'}
		r = self.session.get(securl, headers= headers)
		return r

	def get_aircraft_by_flight_controller_id(self, registered_flight_module_id:str):
		''' This method downloads all aircrafts in the management server '''
		securl = self.aerobridge_url + 'registry/aircraft/rfm/' + registered_flight_module_id
		headers = {'Authorization': 'Bearer '+ self.token, 'content-type': 'application/json'}
		
		r = self.session.get(securl, headers= headers)
		return r
		
	def get_firmware_by_flight_controller_id(self, registered_flight_module_id:str):
		''' This method downloads all aircrafts in the management server '''
		
		securl = self.aerobridge_url + 'registry/aircraft/firmware/' + registered_flight_module_id
		headers = {'Authorization': 'Bearer '+ self.token, 'content-type': 'application/json'}
		
		r = self.session.get(securl, headers= headers)
		return r