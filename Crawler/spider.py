import re
import html2text
from unidecode import unidecode
from BeautifulSoup import BeautifulSoup

try:
  import requests
  from requests import async
  from requests import ConnectionError
except ImportError:
  print "Check dependences: python-requests, BeautifulSoup, unidecode is required"
  sys.exit(1)


class Spider (object):

	#
	# @params : html raw html code
	# @return : list links
	#

	def parse_links( cls, html ):

		links = []
		soup = BeautifulSoup(html)

		for link in soup.findAll('a'):
			l = link.get('href')
			if (l):
				links.append(l)

		for link in soup.findAll('frame'):
			l = link.get('src')
			if (l):
				links.append(l)

		for link in soup.findAll('iframe'):
			l = link.get('src')
			if (l):
				links.append(l)

		#return re.findall('<a href="(.*?)">.*?</a>', html)

		return links

	parse_links = classmethod(parse_links);


	#
	# @params: links list raw links 
	# @params: url site url
	# @return: list with the links absolute
	#

	def absolute_url( cls, links, url ):

		response = [];

		for link in links:

			if link[0] == "/" :
				# url  = http://www.cs.buap.mx/~secretaria-academica/horarios.html
				# link = /primavera.html
				# http://www.cs.buap.mx/primavera.html

				ban = 0
				n_u = ''

				for i in url:
					if i == '/' and ban <> 3 :
						ban += 1
					elif ban == 3:
						break
					n_u += i
				response.append( n_u + link[1::1] );

			elif ("http" in link):
				response.append(link);
			else:
				# url  = http://www.cs.buap.mx/~secretaria-academica/horarios.html
				# link = primavera.html
				# url  = http://www.cs.buap.mx/~secretaria-academica/primavera.html
				ban = False
				n_u = ''

				for i in reversed (url):
					if not ban and i == '/':
						ban = True
					if ban:
						n_u += i

				l = n_u[::-1]
				response.append( l  + link );
		
		return response;
	
	absolute_url = classmethod(absolute_url);

	#
	# @params: url site url
	# @params: options bot options
	# @return: Request responde object
	#

	@staticmethod
	def get_source( url, options = {} ):

		params_get = {}
		
		if 'args' in options:
			params_get = args=options['args']
		
		args = dict()
		args.update({'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})

		respuesta = None

		try:

			respuesta = requests.get(url, params=params_get, headers=args, timeout=5)
			respuesta.html = unidecode(respuesta.content)

		except Exception:
			print "[ Page not found ] : " + url
			return None

		if (respuesta.history):
			respuesta = None

		return respuesta


	@staticmethod
	def pdf2Text ( pdf ):

		from pyPdf import PdfFileWriter, PdfFileReader

		with open("/tmp/temp_crawler.pdf", "wb") as file_pdf:
			file_pdf.write( pdf )


		try:
			pdf = PdfFileReader(file("/tmp/temp_crawler.pdf", "rb"))

			content = ""
			for i in range(0,pdf.getNumPages()):
				content += pdf.getPage(i).extractText() + "\n"

			content = u" ".join(content.replace(u"\xa0", u" ").strip().split())

		except Exception:
			print "[ Error con el PDF ]"
			return " "

		return unidecode(content) 

	#
	# @params : 
	# @return : text
	#

	@staticmethod
	def html2text( html ):
		clear_html  = re.sub('<[^<]+?>','',html)
		normalizado = normalize('NFKD',clear_html.decode('utf-8')).encode('ASCII','ignore').lower()
		text        = re.sub(r'[^a-zA-Z\-\ ]','',normalizado)
		text        = re.sub(r'[-_\/]|[a-z]{13,}|\W+|[ \t]+',' ',text)
		return text
		


	#
	# @params: 
	#

	def get_links( cls, response ):
		return cls.absolute_url( cls.parse_links(response.html), response.url);
	get_links = classmethod( get_links )

	# /ruta.hlp
	# ruta.html
	# http://....


