from PIL import Image
import PIL


def image_edition(image):
	im = Image.open('{}.jpg'.format(image))
	im.save('{}.png'.format(image))

	png = '{}.png'.format(image)
	#im=im.rotate(180, expand=True)
	# resizing
	basewidth = 400
	img = Image.open(png)
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img=img.rotate(270, expand=True)
	img.save(png)
	return(png)

def image_edition_1(image):
	im = Image.open('{}.jpg'.format(image))
	im.save('{}.png'.format(image))

	png = '{}.png'.format(image)
	#im=im.rotate(180, expand=True)
	# resizing
	basewidth = 400
	img = Image.open(png)
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img=img.rotate(0, expand=True)
	img.save(png)
	return(png)

def image_edition_2(image):
	png = '{}.png'.format(image)
	#im=im.rotate(180, expand=True)
	# resizing
	basewidth = 400
	img = Image.open(png)
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img.save(png)
	return(png)
