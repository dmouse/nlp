

import re
from datastorage import Stock
from unicodedata import normalize

def html_to_text(data):

	data = data.replace("\n", " ")
	data = data.replace("\r", " ")

	data = " ".join(data.split())

	bodyPat = re.compile(r'< body[^<>]*?>(.*?)< / body >', re.I)
	result = re.findall(bodyPat, data)
	data = result[0]

	print data

	# now remove the java script
	p = re.compile(r'< script[^<>]*?>.*?< / script >')
	data = p.sub('', data)

	# remove the css styles
	p = re.compile(r'< style[^<>]*?>.*?< / style >')
	data = p.sub('', data)

	# remove html comments
	p = re.compile(r'')
	data = p.sub('', data)

	# remove all the tags
	p = re.compile(r'<[^<]*?>')
	data = p.sub('', data)

	return data

db = Stock()
pages = db.visit();
for page in pages:
	try:
		if (page['html'].__len__() > 100):
			html = page['html']
		else:
			html = page['text']

		clear_html  = re.sub('<[^<]+?>','',html)
		normalizado = normalize('NFKD',clear_html.decode('utf-8')).encode('ASCII','ignore').lower()
		text        = re.sub(r'[^a-zA-Z\-\ ]','',normalizado)
		text        = re.sub(r'[-_\/]|[a-z]{13,}|\W+|[ \t]+',' ',text)
		token       = text.split()
		print page['_id'];
		print token

	except Exception:
		continue


#re.sub(r'[-_\/]|[a-z]{13,}|\W+|[ \t]+',' ',re.sub(r'[^a-zA-Z\-\ ]','',normalize('NFKD',(re.sub('<[^<]+?>','',r.content)).decode('utf-8')).encode('ASCII','ignore').lower()))