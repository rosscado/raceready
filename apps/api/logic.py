'''
This module contains business logic for CRUD of resources
It determines how and where to persist server-side resources
'''

from flask_restplus import fields
from api.restplus import api

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
class PeristentModel:
	def __init__(self, db_name):
		self.db = get_db(db_name)

	def get_events(self):
		print("listing documents in events database".format(db.all_docs()))
		all_events = Result(db.all_docs, include_docs=True)
		return [event for event in all_events]

event_status = api.model('Status', {
	'state': fields.String(description='Is the event still on?', enum=['scheduled', 'provisional', 'cancelled', 'confirmed', 'completed'], default='scheduled'),
	'url': fields.String(description='The primary URL where notice of the most recent state change was posted', example='http://www.banbridgecc.com/eventcancellation/')
})

a_club = api.model('Club', {
	'id': fields.Integer(description='The unique identifier of a club (internal)', readonly=True),
	'title': fields.String(required=True, description='The full name of the club', example='Banbridge Cycling Club'),
	'url': fields.String(description="The club's primary web address", example='http://www.banbridgecc.com/')
})

a_circuit = api.model('Circuit', {
	'id': fields.Integer(description='The unique identifier of a circuit (internal)', readonly=True),
	'url': fields.String(description="The route or segment on a route mapping service", example='https://www.strava.com/segments/16848061'),
	'distance_km': fields.Float(description='The length in kilometres of one lap of the circuit', example=7.85),
	'elevation_gain_m': fields.Integer(description='The total elevation gain (ascent) in metres over one lap of the circuit', example=65),
	'flatness_index': fields.Float(description='indicates how close to flat is the circuit', example='0.12', readonly=True)
})

a_course = api.model('Course', {
	'laps': fields.Integer(description='Number of laps of the circuit', example=5),
	'circuit': fields.Nested(a_circuit, description='The course includes one or more laps of this circuit')
})

a_sign_on = api.model('Sign On', {
	'location': fields.String(description='Where is the sign on?', example='Primary School, Donore, Co. Down'),
	'start_time': fields.DateTime(description='When does sign on open? ISO 8601 format: YYMM-MM-DD HH:MM', example='1970-01-01 11:00'),
	'end_time': fields.DateTime(description='When does sign on close? ISO 8601 format: YYMM-MM-DD HH:MM', example='1970-01-01 12:30'),
})

a_stage = api.model('Stage', {
	'title': fields.String(description='The title of the stage or race, especially if different from the headline event', example='John Beggs Memorial Cup'),
	'stage_type': fields.String(description='Is this stage a road race, time trial, etc?', enum=['road race', 'time trial', 'hill climb', 'criterium'], default='road race'),
	'start_time': fields.DateTime(description='What time does the stage start? ISO 8601 format: YYMM-MM-DD HH:MM', example='1970-01-01 13:00'),
	'course': fields.Nested(a_course, description='The race course: the circuit*laps + any other segments')
})

a_contact = api.model('Contact', {
	'name': fields.String(description='Name of a person who can be contacted about the event', example='Christian Schmitz'),
	'email': fields.String(description="Email address at which the contact can be reached", example='asotv@aso.fr'),
	'phone': fields.String(description='Phone number at which the contact can be reached', example='555 593 9323')
})

organisers = api.model('Organisers', {
	'club': fields.Nested(a_club, description='Club hosting the event'),
	'contacts': fields.List(fields.Nested(a_contact, description='A list of persons to contact about the event'))
})

an_event = api.model('Base Event', {
	'id': fields.Integer(description='The unique identifier of an event (internal)', readonly=True),
	'title': fields.String(required=True, description='The name of the event as promoted publically', example='The John Beggs Memorial'),
	'date': fields.Date(required=True,description='When will the event take place? ISO 8601 format: YYYY-MM-DD', example='2018-08-11'),
	'url': fields.String(description='The primary URL promoting the event', example='http://www.banbridgecc.com/thebeggs18/'),
	'location': fields.String(description='The address of the event. Should identify at least the town.', example='Donore, Co. Down'),
	'event_type': fields.String(required=True,description='Is the event a road race, time trial, etc?', enum=['road race', 'time trial', 'hill climb', 'criterium', 'stage race'], default='road race'),
	'status': fields.Nested(event_status, description='Records any schedule changes. If absent assume event is still scheduled normally'),
	'organised_by': fields.Nested(organisers, description='Group (club and persons) organising the event')
})

one_day_event = api.inherit('One Day Event', an_event, {
	'sign_on': fields.Nested(a_sign_on, description='When and where is the sign on?'),
	'races': fields.List(fields.Nested(a_stage, description='Races taking place at the event'))
})

each_day = api.model('Day', {
	'sign_on': fields.Nested(a_sign_on, description="Today's sign on"),
	'stages': fields.List(fields.Nested(a_stage, description="Today's stages"))
})

multi_day_event = api.inherit('Multi Day Event', an_event, {
	'days': fields.List(fields.Nested(each_day))
})

data_store = TransientModel()
