

import re
from datastorage import Stock

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

for page in db.visit():
	try:

		print html_to_text(page['html'])

	except Exception:
		continue
