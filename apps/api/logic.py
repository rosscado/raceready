'''
This module contains business logic for CRUD of resources
It determines how and where to persist server-side resources
'''

class TransientModel:
	def __init__(self):
		self.events = []
		self.clubs = []
		self.circuits = []

	# event related functions
	def get_events(self):
		return self.events

	def create_event(self, payload):
		#doc = db_client.create_document(api.payload)
		self.events.append(payload)
		doc = payload
		doc['id'] = len(self.events)
		return doc

	def get_event(self, id):
		if 0 < id <= len(self.events):
			return self.events[id-1]
		else:
			return None

	def update_event(self, id, payload):
		self.events[id-1] = payload

	def delete_event(self, id):
		del self.events[id-1]

	# club related functions
	def get_clubs(self):
		return self.clubs

	def create_club(self, payload):
		#doc = db_client.create_document(api.payload)
		self.clubs.append(payload)
		doc = payload
		doc['id'] = len(self.clubs)
		return doc

	def get_club(self, id):
		if 0 < id <= len(self.clubs):
			return self.clubs[id-1]
		else:
			return None

	def update_club(self, id, payload):
		self.clubs[id-1] = payload

	def delete_club(self, id):
		del self.clubs[id-1]

	# circuit related functions
	def _add_flatness_index(self, c):
		'''Compute the flatness_index and add to circuit object c if not already present'''
		if 'distance_km' in c and 'elevation_gain_m' in c and 'flatness_index' not in c:
			c['flatness_index'] = c['distance_km']/c['elevation_gain_m']

	def get_circuits(self):
		for circuit in self.circuits:
			self._add_flatness_index(circuit)
		return self.circuits

	def create_circuit(self, payload):
		#doc = db_client.create_document(api.payload)
		self.circuits.append(payload)
		doc = payload
		doc['id'] = len(self.circuits)
		return doc

	def get_circuit(self, id):
		if 0 < id <= len(self.circuits):
			c = self.circuits[id-1]
			self._add_flatness_index(c)
			return c
		else:
			return None

	def update_circuit(self, id, payload):
		self.circuits[id-1] = payload

	def delete_circuit(self, id):
		del self.circuits[id-1]

from database.clients import get_db
from cloudant.result import Result
class PersistentModel:
	def __init__(self, db_name):
		self.db = get_db(db_name)

	def get_events(self):
		print("listing documents in events database".format(db.all_docs()))
		all_events = Result(db.all_docs, include_docs=True)
		return [event for event in all_events]


data_store = TransientModel()
