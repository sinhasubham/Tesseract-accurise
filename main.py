import io
from PIL import Image, ImageEnhance
import pytesseract
from wand.image import Image as wi
import os
import sys
import pdfminer

def enhancer(im):
	enhancer = ImageEnhance.Contrast(im)
	enhanced_im = enhancer.enhance(2.0)
	enhancer3 = ImageEnhance.Sharpness(enhanced_im)
	enhanced_im3 = enhancer3.enhance(5)
	return enhanced_im3

try:
	FILE=sys.argv[1]
except Exception as e:
	print("Usage: python main.py pdffile")
	sys.exit(2)

if not (os.path.exists(FILE) and not os.path.isdir(FILE)):
	print("Path doesn't exist")
	sys.exit(2)

with wi(filename=FILE, resolution=300) as pdf:
	count = 1
	for page in pdf.sequence:
		page_img = wi(page)
		with page_img.convert('jpeg') as jpgs:
			print(jpgs)
			pimg = Image.open(io.BytesIO(jpgs.make_blob('jpeg')))
			en_img = enhancer(pimg)

			txt_pdf = pytesseract.image_to_pdf_or_hocr(en_img, extension='pdf')
			with open(f"res-{count}.pdf", "wb") as fp:
				fp.write(txt_pdf)

			os.system(f"pdf2txt.py -o res-{count}.html res-{count}.pdf")
			count+=1