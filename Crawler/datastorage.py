import pymongo
from pymongo import Connection

class Stock (object):

	connection = None;
	collection = None;
	db = None;


	#
	#
	#

	def __init__( self ):

		try:
			self.connection = Connection('localhost', 27017);
			self.db = self.connection.nlp;
			self.collection = self.db.crawler;
		except ImportError:
			print "Conexion fallida"
			sys.exit(1)


	#
	#
	#

	def save_data(self, data):
		return self.collection.insert(data);

	#
	# @params: data value collections
	# @return: mongo object 
	#

	def update(self, data ):
		return self.collection.update( {'_id': data['_id'] } ,data )

	
	#
	#
	#

	def exist_url(self, url):
		return self.collection.find_one( { 'url' : url } );

	#
	# @params: url link to page
	# @return: list with data url ['visit']
	#

	def visit_url(self, url):
		return self.collection.find_one( { 'url' : url }, { 'visit' : 1} );

	#
	# @return one element not visited
	#

	def url ( self ):
		return self.collection.find_one( { 'visit' : False, 'url': {'$regex':'^(http://[a-zA-Z0-9.-]{3,15}\.cs\.buap\.mx)'} } );

	# 
	# @return one element visited
	#

	def visit(self):
		return self.collection.find( {'$where':'this.text.length > 0 ', 'visit' : True, 'url': {'$regex' :'^(http://[a-zA-Z0-9.-]{3,15}\.cs\.buap\.mx)'} } ).limit(10)
		#return self.collection.find({'$where':'this.text.length > 0 '})

	#
	#
	#

	def checksum(self,checksum):
		return self.collection.find_one( { 'checksum' : checksum } );