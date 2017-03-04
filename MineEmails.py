import urlparse
import urllib
import json
from bs4 import BeautifulSoup

def scrapeQuery(url):
	# Goal is to find the Builder's Houzz profile
	print 'Currently scraping: ' + url

	htmltext = urllib.urlopen(url).read()
	soup = BeautifulSoup(htmltext, "html.parser")
	for link in soup.find_all('a', {'class': 'pro-title'}) : 
		# BeautifulSoup may have a bug that incorrectly grabs elements. 
		# Check for and toss out the bad ones
		if link['href'] != 'javascript:;' :
			urls.append(str(link['href']))
	return


def scrapeBuilderPage(url):
	# Goal is to find the builder website
	print 'Scraping Builder Houzz Page: ' + url

	htmltext = urllib.urlopen(url).read()
	soup = BeautifulSoup(htmltext, "html.parser")
	for link in soup.find_all('a', {'class': 'proWebsiteLink'}) : 
		websites.append(str(link['href']))
		# print str(link['href'])

	return

def scrapeBuilderWebsite(website):
	# Goal is to find an email address
	# print website
	subdirs = []
	print 'Scraping: ' + website

	htmltext = urllib.urlopen(website).read()
	soup = BeautifulSoup(htmltext, "html.parser")
	for link in soup.find_all( ['a','img'] , href=True) :
		# Search for top level emails
		scrapeForEmail(link)
		print link['href']
		# Search for subdirectories

		if str(link['href']).find(website[6:]) > -1:

			print 'Scraping SubDirectory: ' + link['href']
			htmltext = urllib.urlopen(link['href']).read()
			soup = BeautifulSoup(htmltext, "html.parser")

			for sublink in soup.find_all('a',href=True) :
				# Search for top level emails
				scrapeForEmail(sublink)

		if str(link['href']).find('contact') > -1:
			print 'Scraping SubDirectory: ' + website + '/' + link['href']
			htmltext = urllib.urlopen(website + '/' + link['href']).read()
			soup = BeautifulSoup(htmltext, "html.parser")

			for sublink in soup.find_all('a',href=True) :
				# Search for top level emails
				scrapeForEmail(sublink)

		elif str(link['href']).find('about') > -1:
			print 'Scraping SubDirectory: ' + website + '/' + link['href']
			htmltext = urllib.urlopen(website + '/' + link['href']).read()
			soup = BeautifulSoup(htmltext, "html.parser")

			for sublink in soup.find_all('a',href=True) :
				# Search for top level emails
				scrapeForEmail(sublink)

		elif str(link['href']).find('team') > -1:
			print 'Scraping SubDirectory: ' + website + '/' + link['href']
			htmltext = urllib.urlopen(website + '/' + link['href']).read()
			soup = BeautifulSoup(htmltext, "html.parser")

			for sublink in soup.find_all('a',href=True) :
				# Search for top level emails
				scrapeForEmail(sublink)

	return

def scrapeForEmail(link) :
	index = str(link['href']).find('mailto:')
	if index > -1:
		index2 = str(link['href']).find('@')
		if index2 > -1:
			emails.append(str(link['href'][7:]))
			print 'FOUND EMAIL! : ' + str(link['href'][7:])
	return


url = "http://www.houzz.com/professionals/design-build/c/"
city = "San Francisco"
state = "CA"
numPages = 20

urls = []
websites = []
emails = []
currentPage = 1

while currentPage <= numPages :
	currentUrl = url + city + '--' + state + '/p/' + str(currentPage * 15 - 15)
	scrapeQuery(currentUrl)
	currentPage += 1

for url in urls : 
	scrapeBuilderPage(url)

for website in websites : 
	try :
		scrapeBuilderWebsite(website)
	except :
		continue

cleaned = list(set(emails))
with open(city + '--' + state + '.csv', 'wb') as csvfile:
	for e in cleaned :
		csvfile.write(str(e) + ',\n')
		print str(e)