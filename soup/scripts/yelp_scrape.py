
from bs4 import BeautifulSoup

from urllib import request

import time

import re

import pathlib


url = "https://www.yelp.com/search?find_desc=&find_loc=Boston%2C+MA&ns=1" #("https://www.yelp.com/boston")

page = request.urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

#print(soup.prettify())

#print(soup.get_text())

#default setting for radius of 5 miles from user location ("convenient")

businesses = []

for ul in soup.find_all('ul'):
	#print(ul.get('class'))
	if ul.get('class') and "ylist" in ul.get('class'):
		for li in ul.find_all('li'):
			if li and 'regular-search-result' in li.get('class'):
				print(li.a.get('href'))
				businesses.append(li.a.get('href')[5:len(li.a.get('href'))])

print(businesses)

#grab pictures from these businesses
#save in "../img/(biz-name)/(img.jpg)"

pattern = re.compile(r'^(.*)/[^/]*[.][^/]*$')
img_name_p = re.compile(r'^.*/([^/]*)')

for biz in businesses[4:6]:
	# don't overload the server
	time.sleep(.5)

	image_page = request.urlopen("https://www.yelp.com/biz_photos/"+biz+"?tab=food")

	image_soup = BeautifulSoup(image_page, 'html.parser')

	for div in image_soup.find_all('div'):
		if div and div.get('class') and "photos" in div.get('class'):
			for img in div.find_all('img'):
				#add /o.jpg to view original image, full-res
				image_addr = img.get('src')
				m = pattern.match(image_addr)
				if m:
					img_url = m.groups()[0] + "/o.jpg"
					img_name = img_name_p.match(m.groups()[0]).groups()[0]
					img_save_path = "../img/" +biz+ "/"
					img_save_file = img_save_path +img_name + ".jpg"
					
					#make sure path exists

					pathlib.Path(img_save_path).mkdir(parents=True, exist_ok=True)

					time.sleep(.5)
					request.urlretrieve(img_url, img_save_file)
				#original_addr = image_addr

'''
for link in soup.find_all('a'):
	#if "food" in line:
	href = link.get('href')
	if href == "/biz/sam-lagrassas-boston-3":
		print(link)
		#save image inside link
		for img in link.find_all('img'):
			request.urlretrieve( img.get('src'), "../img/" +img.get('alt') + ".jpg")
'''
#so I should grab pictures using the menu for the specific restaurants
