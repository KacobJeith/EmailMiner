from __future__ import division
import os
import sys
import urlparse
import urllib
import time
import json
from bs4 import BeautifulSoup

def scrapeQuery(url):
	# Goal is to find the Builder's Houzz profile
	print 'Currently scraping: ' + url

	htmltext = urllib.urlopen(url).read()
	soup = BeautifulSoup(htmltext, "html.parser")
	for link in soup.find_all('a', {'class': 'pro-title'}) : 
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

	hits = 0
	print 'Scraping: ' + website

	htmltext = urllib.urlopen(website).read()
	soup = BeautifulSoup(htmltext, "html.parser")
	stats['pagesScraped'] += 1

	for link in soup.find_all( ['a','img'] , href=True) :
		# Search for top level emails
		hits += scrapeForEmail(link)
		print link['href']

		# Search for subdirectories
		if any(x in str(link['href']) for x in ['contact', 'about', 'team', 'people']) : 

			if any(x in str(link['href']) for x in ['http:', 'https:']) : 
				hits += searchSubdirectory(link['href'])
			else :
				hits += searchSubdirectory( website + '/' + link['href'])
		
	if hits > 0 :
		stats['websitesWithEmails'] += 1

	return

def searchSubdirectory(linkref) :
	print 'Scraping SubDirectory: ' + linkref
	htmltext = urllib.urlopen(linkref).read()
	soup = BeautifulSoup(htmltext, "html.parser")
	stats['pagesScraped'] += 1
	hits = 0

	for sublink in soup.find_all('a',href=True) :
		# Search for top level emails
		hits += scrapeForEmail(sublink)

	return hits

def scrapeForEmail(link) :
	index = str(link['href']).find('mailto:')

	if index > -1:
		index2 = str(link['href']).find('@')
		if index2 > -1:
			emails.append(str(link['href'][7:]))
			print ':::::::::::::::::::::EMAIL:::::::::::::::::::::' + str(link['href'][7:])
			return 1

	return 0


start_time = time.time()

url = "http://www.houzz.com/professionals/design-build/c/"
city = sys.argv[1]
state = sys.argv[2]
numPages = int(sys.argv[3])

urls = []
websites = []
emails = []
currentPage = 1

stats = {'expectedProfiles': 0, 
		 'profiles': 0, 
		 'websites': 0, 
		 'pagesScraped': 0, 
		 'websitesWithEmails': 0, 
		 'emails': 0}

stats['expectedProfiles'] = numPages*15

while currentPage <= numPages :
	currentUrl = url + city + '--' + state + '/p/' + str(currentPage * 15 - 15)
	scrapeQuery(currentUrl)
	currentPage += 1

stats['profiles'] = len(urls)

for url in urls[7:] : 
	scrapeBuilderPage(url)

stats['websites'] = len(websites)

for website in websites : 
	try :
		scrapeBuilderWebsite(website)
	except :
		continue

cleaned = list(set(emails))
stats['emails'] = len(cleaned)

if os.path.isdir(os.path.join(os.getcwd(), 'results')) == False:
	os.makedirs(os.path.join(os.getcwd(), 'results'))

if os.path.isdir(os.path.join(os.getcwd(), 'logs')) == False:
	os.makedirs(os.path.join(os.getcwd(), 'logs'))

path = os.path.join(os.getcwd(), 'results', city + '--' + state + '.csv')
logpath = os.path.join(os.getcwd(), 'logs', city + '--' + state + '.txt')

with open(path, 'wb') as csvfile:
	for e in cleaned :
		csvfile.write(str(e).strip() + ',\n')
		print str(e)

end_time = time.time()

logfile = open(logpath, 'ab+')
logfile.write(':::::::::::::::::::::' + time.strftime("%Y-%m-%d %H:%M") + ':::::::::::::::::::::' + '\n')
logfile.write('Results stored at: '+ path + '\n')
logfile.write('Expected Number Houzz Profiles: ' + str(stats['expectedProfiles']) + '\n')
logfile.write('Discovered Number Houzz Profiles: ' + str(stats['profiles']) + '\n')
logfile.write('Profile Discovery Rate: ' + str(stats['profiles'] / stats['expectedProfiles'] * 100) + '%' + '\n')
logfile.write('Number of Websites Discovered: ' + str(stats['websites']) + '\n')
logfile.write('Website Discovery Rate: ' + str(stats['websites'] / stats['profiles'] * 100) + '%' + '\n')
logfile.write('Number of Pages Scraped: ' + str(stats['pagesScraped']) + '\n')
logfile.write('Average Pages per Website: ' + str(stats['pagesScraped'] / stats['websites']) + '\n')
logfile.write('Total Emails Discovered: ' + str(stats['emails']) + '\n')
logfile.write('Total Websites with Emails Discovered: ' + str(stats['websitesWithEmails']) + '\n')
logfile.write('Emails Discovery Rate per Website: ' + str(stats['websitesWithEmails'] / stats['websites'] * 100) + '%' + '\n')
logfile.write('Overall Email Discovery Rate: ' + str(stats['websitesWithEmails'] / stats['expectedProfiles'] * 100) + '%' + '\n')
logfile.write('Total Runtime: %g seconds' % (end_time - start_time)  + '\n')
logfile.write('Runtime per Website: ' + str((end_time - start_time) / stats['websites']) + ' seconds' + '\n\n')










