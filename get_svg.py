import re
import numpy as np
import sys
import os

num_related_query = 15
query_list = ["education", 'health', 'finance', 'science', 'politics', 'social', 'media', 'sports', 'global', 'marketing']


def get_page_link(query):
	query_list = query.split(' ')
	temp = 'infographics'
	for i in range(0,len(query_list)):
		temp += '+'+query_list[i]
	return ("https://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q="+temp+"&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=ift:svg#imgrc=5r2syL9GXxKrIM")

def download(link, filename):
	cmd = "wget -O "+filename+" -U \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36\" \""+link+"\""
	os.system(cmd)

def create_dir(directory):
	cmd = "mkdir "+directory+""
	os.system(cmd)	

def get_image_links(html_filename):
	image_links = []
	for i, line in enumerate(open(html_filename)):
		image_links += re.findall(r'(http|https)\://(.+?)(.svg|\")', line)
	return image_links

def get_related_queries(html_filename):
	related_query = []
	for i, line in enumerate(open(html_filename)):
		related_query += re.findall(r'\[\"[a-z]+\"\,\[\"https\:.+\"', line)
	return [related_query[i][1:].split(",")[0].strip('"') for i in range(num_related_query)]

def download_images(image_links, directory):
	file_count = 1
	for link in image_links:
		if(link[-1]==".svg"):
			url = link[0] + '://'+ link[1] + link[2]

			filename = directory+'/'+str(file_count)+'.svg'
			try:
				download(url, filename)
			except:
				print('******* could not download*********')
			# print(url)
			# print('------')
			file_count+=1

def download_image_for_query(query):
	page_link = get_page_link(query)
	
	filename = ''
	for ele in query.split(' '):
		filename = filename+ele

	html_filename = "./query_results/"+filename+'.html'
	download(page_link, html_filename)

	image_links = get_image_links(html_filename)

	directory = './svg/'+filename
	create_dir(directory)
	download_images(image_links, directory)
	return html_filename


for original_query in query_list:
	html_filename = download_image_for_query(original_query)
	related_queries = get_related_queries(html_filename)

	for query in related_queries:
		download_image_for_query(query)