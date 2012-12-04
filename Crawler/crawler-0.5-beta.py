import time 
#import nltk # NLP 
import hashlib

from spider import Spider     # Clase para visitar los sitios web
from datastorage import Stock # Interactua con mongodb

from unidecode import unidecode

stop = True
db = Stock() # instancia para almacenamiento


while( stop ):

	if ( not db.url() ):
		break

	site = db.url()     # obtenemos una url no visitada 
	url  = site['url']  # separo la url
	m    = hashlib.sha1()
	date = time.strftime("%Y-%m-%d %H:%m")

	print "[ Visit  ] " + url 

	response = Spider.get_source(url) # obtiene el html de la url


	if not response :         #si no hay respuesta lo marca como visitado
		site['visit'] = True
		db.update(site)	    # updatea el url 
		continue			  # y continua

	if 'application/pdf' in response.headers['content-type'] :

		text = Spider.pdf2Text(response.content)
		html = ''

		m.update(text) 
		checksum = m.hexdigest()

		if db.checksum(checksum):
			site['visit'] = True
			db.update(site)	    # updatea el url 
			continue

		#print '[ PDF ]'

	elif 'text/html' in response.headers['content-type'] :

		html  = response.html

		m.update(html)
		checksum = m.hexdigest()

		if db.checksum(checksum):
			site['visit'] = True
			db.update(site)	    # updatea el url 
			continue

		text =  Spider.html2text(response.html) 

		links = Spider.get_links( response ) # obtiene la lista de links dentro del html 

		for link in links: 
			link = unidecode( link )
			if not db.exist_url( link ):
				save = {
					'url'      : link    ,
					'reference': [ url ] , # referencia con id
					'text'     : ''      ,
					'html'	   : ''      ,
					'visit'	   : False   ,
					'date'     : date    ,
				}
				db.save_data(save); # Guarda el link nuevo
				print "[  Save  ] " + link

		#print '[ html ]'

	else :
		site['visit'] = True
		db.update(site)      	# updatea el url 
		#print '[ VS ]'
		continue			  	# y continua

	site['visit']    = True
	site['text']     = text
	site['html']     = html
	site['date']     = date
	site['checksum'] = checksum

	db.update ( site )   # update de la url visitada
	print "[ Update ] " + url

	if ( not db.url() ):
		stop = False