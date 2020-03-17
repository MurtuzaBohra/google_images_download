import os

svg_dir = './svg/'
png_dir = './png/'

def create_dir(directory):
	cmd = "mkdir "+directory+""
	os.system(cmd)

all_dir = os.listdir(svg_dir)

for directory in all_dir:

	svg_filename = svg_dir+directory+'/'
	png_filename = png_dir+directory+'/'
	create_dir(png_filename)

	files = os.listdir(svg_filename)

	for file in files:

		try:
			cmd = "inkscape -z -e "+png_filename+file.rstrip('.svg')+'.png'+" -w 1024 -b \'#ffffff\' "+svg_filename+file+""
			os.system(cmd)
		except:
			print('***could not convert***')
	print('******************************')

