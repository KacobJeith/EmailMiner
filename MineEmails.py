from __future__ import division
import os
import sys
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

		if str(link['href']).find(website[6:]) > -1:

			print 'Scraping SubDirectory: ' + link['href']
			htmltext = urllib.urlopen(link['href']).read()
			soup = BeautifulSoup(htmltext, "html.parser")
			stats['pagesScraped'] += 1

			for sublink in soup.find_all('a',href=True) :
				# Search for top level emails
				hits += scrapeForEmail(sublink)
				

		elif str(link['href']).find('contact') > -1:
			print 'Scraping SubDirectory: ' + website + '/' + link['href']
			htmltext = urllib.urlopen(website + '/' + link['href']).read()
			soup = BeautifulSoup(htmltext, "html.parser")
			stats['pagesScraped'] += 1			

			for sublink in soup.find_all('a',href=True) :
				# Search for top level emails
				hits += scrapeForEmail(sublink)

		elif str(link['href']).find('about') > -1:
			print 'Scraping SubDirectory: ' + website + '/' + link['href']
			htmltext = urllib.urlopen(website + '/' + link['href']).read()
			soup = BeautifulSoup(htmltext, "html.parser")
			stats['pagesScraped'] += 1

			for sublink in soup.find_all('a',href=True) :
				# Search for top level emails
				hits += scrapeForEmail(sublink)

		elif str(link['href']).find('team') > -1:
			print 'Scraping SubDirectory: ' + website + '/' + link['href']
			htmltext = urllib.urlopen(website + '/' + link['href']).read()
			soup = BeautifulSoup(htmltext, "html.parser")
			stats['pagesScraped'] += 1

			for sublink in soup.find_all('a',href=True) :
				# Search for top level emails
				hits += scrapeForEmail(sublink)

	if hits > 0 :
		stats['websitesWithEmails'] += 1

	return

def scrapeForEmail(link) :
	index = str(link['href']).find('mailto:')

	if index > -1:
		index2 = str(link['href']).find('@')
		if index2 > -1:
			emails.append(str(link['href'][7:]))
			print 'FOUND EMAIL! : ' + str(link['href'][7:])
			return 1

	return 0


url = "http://www.houzz.com/professionals/design-build/c/"
city = sys.argv[1]
state = sys.argv[2]
numPages = int(sys.argv[3])

urls = []
websites = []
emails = []
currentPage = 1

stats = {'expectedProfiles': 0, 'profiles': 0, 'websites': 0, 'pagesScraped': 0, 'websitesWithEmails': 0, 'emails': 0}
stats['expectedProfiles'] = numPages*15

while currentPage <= numPages :
	currentUrl = url + city + '--' + state + '/p/' + str(currentPage * 15 - 15)
	scrapeQuery(currentUrl)
	currentPage += 1

stats['profiles'] = len(urls)

for url in urls : 
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
path = os.path.join(os.getcwd(), 'results', city + '--' + state + '.csv')
with open(path, 'wb') as csvfile:
	for e in cleaned :
		csvfile.write(str(e).strip() + ',\n')
		print str(e)

print ':::::Scanning Complete:::::'
print 'Results stored at: '+ path
print 'Expected Number Houzz Profiles: ' + str(stats['expectedProfiles'])
print 'Discovered Number Houzz Profiles: ' + str(stats['profiles'])
print 'Profile Discovery Rate: ' + str(stats['profiles'] / stats['expectedProfiles'] * 100) + '%'
print 'Number of Websites Discovered: ' + str(stats['expectedProfiles'])
print 'Website Discovery Rate: ' + str(stats['websites'] / stats['profiles'] * 100) + '%'
print 'Number of Pages Scraped: ' + str(stats['pagesScraped'])
print 'Average Pages per Website: ' + str(stats['pagesScraped'] / stats['websites'])
print 'Total Emails Discovered: ' + str(stats['emails'])
print 'Total Websites with Emails Discovered: ' + str(stats['websitesWithEmails'])
print 'Emails Discovery Rate per Website: ' + str(stats['emails'] / stats['websites'] * 100) + '%'
print 'Overall Email Discovery Rate: ' + str(stats['emails'] / stats['expectedProfiles'] * 100) + '%'