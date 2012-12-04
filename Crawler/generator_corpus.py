import re
from datastorage import Stock

db = Stock()

for page in db.visit():

	try:

		page['text'] = u" ".join(page['text'].replace(u"\xa0", u" ").strip().split())
		print str(page['_id']) + " " + re.sub(r'[-_\/]',' ',re.sub(r'[^a-zA-Z\-\ ]', '', page['text'].lower() ))

	except Exception:
		continue
		
