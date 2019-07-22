from PIL import Image
import requests
from io import BytesIO

class ImageHandler:
	cache = []

	def loadImage(name):
		try: 
			img = Image.open("Images/"+ name +".png")
			ImageHandler.cache.append(name)
			#print("Image Local")
		except:
			url = "http://ddragon.leagueoflegends.com/cdn/9.13.1/img/champion/"+ name +".png"
			response = requests.get(url)
			img = Image.open(BytesIO(response.content))
			img.save("Images/"+ name +".png","PNG")
			ImageHandler.cache.append(name)
			#print("Image Downloaded")

	def formatNames(names):
		outNames = []
		for name in names:
			outNames.append(name.replace(" ",""))
		return outNames

	def makeDraft(names):
		for name in names:
			ImageHandler.loadImage(name)
		picks = len(names)
		fileNames = []
		for name in names:
			fileNames.append("Images/"+ name + ".png")
		images = map(Image.open, fileNames)
		height = len(fileNames) * 120
		new_im = Image.new('RGB', (120, 600))
		offset = 0
		for img in images:
			new_im.paste(img, (0,offset))
			offset += 120
		empty = Image.open("Images/Empty.png")
		for i in range(5 - picks):
			new_im.paste(empty, (0,offset))
			offset += 120
		new_im.show()

	def makeBans(names):
		for name in names:
			ImageHandler.loadImage(name)
		picks = len(names)
		fileNames = []
		for name in names:
			fileNames.append("Images/"+ name + ".png")
		images = map(Image.open, fileNames)
		height = len(fileNames) * 120
		new_im = Image.new('RGB', (600, 120))
		offset = 0
		for img in images:
			new_im.paste(img, (offset,0))
			offset += 120
		empty = Image.open("Images/Empty.png")
		for i in range(5 - picks):
			new_im.paste(empty, (offset,0))
			offset += 120
		new_im.show()


raw_names = ["Anivia", "Tahm Kench", "Galio"]
names = ImageHandler.formatNames(raw_names)
ImageHandler.makeBans(names)