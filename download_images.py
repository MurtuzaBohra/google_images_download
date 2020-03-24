import re
import numpy as np
import sys
import os
import cloudpickle as pickle

num_related_query = 15
query_list = ["","education", 'health', 'finance', 'science', 'politics', 'social', 'media', 'sports', 'global', 'marketing', 'demographics']
image_links_global = []
count_all = 0

def get_page_link(query):
	query_list = query.split(' ')
	temp = 'infographics'
	for i in range(0,len(query_list)):
		temp += '+'+query_list[i]
	#for all formats
	output = "https://www.google.com/search?q="+temp+"&source=lnms&tbm=isch&sa=X&ved=2ahUKEwig7r2v4rLoAhUF7XMBHXqjAhsQ_AUoAXoECBUQAw&biw=1301&bih=672"

	#for only svg files
	# output = "https://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q="+temp+"&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=ift:svg#imgrc=5r2syL9GXxKrIM"
	return (output)

def download(link, filename):
	cmd = "wget -O "+filename+" -U \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36\" \""+link+"\""
	os.system(cmd)

def create_dir(directory):
	cmd = "mkdir "+directory+""
	os.system(cmd)	

def remove_duplicate(image_links):
	global image_links_global

	unique_links = []
	for link in image_links:
		if link not in image_links_global:
			unique_links.append(link)
			image_links_global.append(link)
	return unique_links

def get_image_links(html_filename):
	global count_all

	image_links = []
	for i, line in enumerate(open(html_filename)):
		#for only svg files
		# image_links += re.findall('(https)\://([^\"]+)(\.svg\")', line)

		#for all formats
		image_links += re.findall('(https)\://([^\"]+)(\.(svg|png|jpg|jpeg|bmp)\")', line)

	count_all += len(image_links)
	image_links = remove_duplicate(image_links)
	return image_links

def get_related_queries(html_filename):
	related_query = []
	for i, line in enumerate(open(html_filename)):
		related_query += re.findall(r'\[\"[a-z]+\"\,\[\"https\:.+\"', line)
	return [related_query[i][1:].split(",")[0].strip('"') for i in range(min(len(related_query),num_related_query))]

def download_images(image_links, directory):
	file_count = 1
	for link in image_links:
		url = link[0] + '://'+ link[1] + link[2]
		url = url.strip('\"')

		# if(link[-1]==".svg\""):
		filename = directory+'/'+str(file_count)+link[-1].rstrip('"')
		try:
			download(url, filename)
		except:
			print('******* could not download*********')
		file_count+=1


def save_list_of_downloaded_images():
	global image_links_global

	temp = []
	for link in image_links_global:
		url = link[0] + '://'+ link[1] + link[2]
		url = url.strip('\"')
		temp.append(url)
	pickle.dump(temp, open('../url_of_downloaded_images_all_formats.txt', 'wb'))


def download_image_for_query(query):

	page_link = get_page_link(query)
	
	query_term = ''
	for ele in query.split(' '):
		query_term = query_term+ele

	html_filename = "../query_results/"+query_term+'.html'
	download(page_link, html_filename)

	image_links = get_image_links(html_filename)
	save_list_of_downloaded_images()
	print(len(image_links),' images will be downloaded')

	directory = '../all_format_images/'+query_term
	try:
		create_dir(directory)
		download_images(image_links, directory)
	except:
		print('*****repeated related query*******')
	return html_filename

#------------------------------------------------------------------
#------------------------------------------------------------------
all_queries_list = []
for original_query in query_list:
	if(original_query not in all_queries_list):
		all_queries_list.append(original_query)
		html_filename = download_image_for_query(original_query)

		print('--------------')
		print('count_all, unique', count_all, len(image_links_global))
		print('--------------')

		related_queries = get_related_queries(html_filename)

		for query in related_queries:
			if(original_query not in all_queries_list):
				all_queries_list.append(query)
				download_image_for_query(query)
				print('--------------')
				print('count_all, unique', count_all, len(image_links_global))
				print('--------------')
			else:
				print('*********QUERY REPEATED***********')
	else:
		print('*********QUERY REPEATED***********')

#------------------------------------------------------------------
#------------------------------------------------------------------
