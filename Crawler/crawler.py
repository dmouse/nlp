import time 
import nltk # NLP 

from spider import Spider     # Clase para visitar los sitios web
from datastorage import Stock # Interactua con mongodb

from unidecode import unidecode

url = "http://www.cs.buap.mx"

unsupported = ['jpg','png','ppt','mailto','gif','xls','rar','zip','tar.gz','gz', 
'digg','facebook','del','stumbleupon','google','twitter','linkedin','yahoo','faves']


stop = True
db = Stock() # instancia para almacenamiento

while ( stop ):

	site = db.url()     # obtenemos una url no visitada 
	url  = site['url']  # separo la url


	print "visitando: " + url 

	page = db.exist_url( url )
	
	if ( any( tipo in url for tipo in unsupported) ): # checa si es un elemento no soportado
		page['visit'] = True  # dice que ya lo visito
		db.update(page)       # y hace update y continua con el siguiente link
		continue


	response = Spider.get_source(url) # obtiene el html de la url


	if not response :         #si no hay respuesta lo marca como visitado
		page['visit'] = True  
		#TODO : guardar el error por el cual no se pudo visitar la pagina
		db.update(page)      # updatea el url 
		continue			  # y continua


	links = Spider.get_links( response ) # obtiene la lista de links dentro del html 

	#
	# Inicializacion de variables
	#

	if response.headers['content-type'] == 'application/pdf':
		text = Spider.pdf2Text(response.content)
		html = ''
	else:
		text = unidecode( Spider.html2text(response.html) ) 
		html  = response.html
		print response.headers['content-type']
		break

	visit = True 
	#token = nltk.word_tokenize( text )
	date  = time.strftime("%Y-%m-%d %H:%m")

	# update del valores

	# TODO: Reference update

	site['visit']  = visit
	site['text']   = text
	site['html']   = html
	#site['tokens'] = token
	site['date']   = date
	
	db.update ( site )   # update de la url visitada
	print "[ Update ] : " + url

	# Ahora guardamos los liks que obtuvimos en la pagina

	for link in links: 

		link = unidecode( link )

		# Si no existe en la base de datos y el formato es soportado 
		if ( not db.exist_url( link ) and ( not ( any(tipo in link for tipo in unsupported) ) ) ) : 

			save = {
				'url'      : link    ,
				'reference': [ url ] ,
				'text'     : ''      ,
				'html'	   : ''      ,
	#			'tokens'   : []      ,
				'visit'	   : False   ,
				'date'     : date    ,
			};

			db.save_data(save); # Guarda el link nuevo
			
			print "[  Save  ] : " + link

	#print time.localtime();
	#time.sleep(2);

	if ( not db.url() ):
		stop = False

	#stop += 1