#used to manipulate images before uploading

def crop(image, filename):
	from wand.image import Image

	with Image(file=image) as img:
		width = img.width
		height = img.height


		#if the width of an image is wider than 4096px, crop the width, but leave the height
		if width > 4096:
			print "Image too wide, cropping width"
			img.crop(0, 0, 4096, height)
			img.save(filename=filename)

		else:
			print "image is less than 4096px wide, saving"
			img.save(filename=filename)
