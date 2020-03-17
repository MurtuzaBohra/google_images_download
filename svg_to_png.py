import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

svg_dir = './svg_2/'
png_dir = './png_2/'

def create_dir(directory):
	cmd = "mkdir "+directory+""
	os.system(cmd)

all_dir = os.listdir(svg_dir)
print('********')
print(all_dir)
print('********')

for directory in all_dir:

	svg_filename = svg_dir+directory+'/'
	png_filename = png_dir+directory+'/'
	create_dir(png_filename)

	files = os.listdir(svg_filename)
	print('--------')
	print(files)
	print('--------')

	for file in files:
		svg_filename = svg_filename+file
		png_filename = png_filename+file.rstrip('.svg')+'.png'

		try:
			drawing = svg2rlg(svg_filename)
			renderPM.drawToFile(drawing, png_filename, fmt="PNG")
		except:
			print('***could not convert***')
	print('******************************')

		

