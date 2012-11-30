import re
from datastorage import Stock

db = Stock()

for page in db.visit():

	try:

		page['text'] = u" ".join(page['text'].replace(u"\xa0", u" ").strip().split())
		print str(page['_id']) + " " + re.sub(r'[-_\/]',' ',re.sub(r'[^a-zA-Z\-\ ]', '', page['text'].lower() ))

	except Exception:
		continue



re.sub(r'[-_\/]|[a-z]{13,}|\W+|[ \t]+',' ',re.sub(r'[^a-zA-Z\-\ ]','',normalize('NFKD',(re.sub('<[^<]+?>','',r.content)).decode('utf-8')).encode('ASCII','ignore').lower()))