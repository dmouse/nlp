
from datastorage import Stock # Interactua con mongodb

db = Stock()

site = db.url()

while( site ):
	#db.update(site)
	site = db.url()
	print site['url']