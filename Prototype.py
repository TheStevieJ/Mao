import csv
import requests
from PIL import Image
from io import BytesIO

class ImageHandler:
	cache = []

	def selectNames(names, nums):
		cheat = [[0,2,4,12,14],[1,3,5,13,15],[6,9,10,17,18],[7,8,11,16,19]]
		outList = []
		total = len(names)
		for x in cheat[nums]:
			if total > x:
				outList.append(names[x])
		return outList

	def loadImage(name):
		try: 
			img = Image.open("Images/"+ name +".png")
			ImageHandler.cache.append(name)
		except:
			url = "http://ddragon.leagueoflegends.com/cdn/9.13.1/img/champion/"+ name +".png"
			response = requests.get(url)
			img = Image.open(BytesIO(response.content))
			img.save("Images/"+ name +".png","PNG")
			ImageHandler.cache.append(name)

	def formatNames(names):
		outNames = []
		for name in names:
			if name is "" or name is "Noban":
				outNames.append("Empty")
			else:
				tempName = name.replace("\'", " ").title()
				tempName = tempName.replace(" ","")
				tempName = tempName.replace("NoBan", "Empty")
				outNames.append(tempName)
		return outNames

	def makeDraft(names, id, num):
		names = ImageHandler.selectNames(names, num)
		names = ImageHandler.formatNames(names)
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
		location = "Images/"+str(id)+".png"
		new_im.save(location)
		return location

	def makeBans(names, id, num):
		names = ImageHandler.selectNames(names, num)
		names = ImageHandler.formatNames(names)
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
		location = "Images/"+str(id)+".png"
		new_im.save(location)
		return location

		def makeNewDraft(names, id, num):


class Pick:
	def __init__(self, name):
		self.name = name
		self.children = []
		self.path = []

	def isChild(self, name):
		for child in self.children:
			if child.name == name:
				return True
		return False

	def addChild(self, name):
		self.children.append(Pick(name))

	def getChild(self, name):
		for child in self.children:
			if child.name == name:
				return child
		return "NULL"

	def getChildren(self):
		return self.children

	def familySize(self):
		return len(self.children)

	def emptyNest(self):
		return not self.children

	def recurPrint(self):
		print(self.name)
		for child in self.children:
			child.recurPrint()


class Tree:
	def __init__(self):
		self.nodes = []
		self.root = Pick("HEAD")

	def __init__(self, name):
		self.nodes = []
		self.root = Pick(name)

	def addDraft(self, insturctions):
		curNode = self.root
		for champ in insturctions:
			if curNode.isChild(champ):
				curNode = curNode.getChild(champ)
			else:
				curNode.addChild(champ)
				curNode = curNode.getChild(champ)

	def printTree(self):
		self.root.recurPrint()

	def getRoot(self):
		return self.root


class MindMap:

	blueBans = [1,3,5,13,15]
	redBans = [2,4,6,14,16]
	bluePicks = [7,10,11,18,19]
	redPicks = [8,9,12,17,20]

	def __init__(self):
		self.name = "NULL"
		self.outFile = "test.mm"
		self.id = 1

	def __init__(self, name):
		self.name = name
		self.outFile = name + ".mm"
		self.id = 1

	def recurWrite(self, node, file, depth, path):
		newPath = path
		newPath.append(node.name)
		color = depth % 2
		if (depth >= 9 and depth <= 10) or (depth >= 17 and depth <= 18):
			color = (color + 1) % 2 
		if color:
			backColor = "#0033ff"
		else:
			backColor = "#ff0033"
		if depth is 0:
			backColor = "#000000"

		if depth is 0:
			file.write("<node HGAP=\"30\" ID=\"ID_"+ str(self.id) +"\" TEXT=\""+ node.name +"\" VSHIFT = \"10\" STYLE = \"bubble\" BACKGROUND_COLOR=\""+ backColor +"\">\n")
			self.id = self.id + 1
			for child in node.getChildren():
				self.recurWrite(child, file, depth + 1, [])
			file.write("</node>\n")
		else:
			link = "Images/Empty.png"
			if depth in MindMap.blueBans or depth in MindMap.redBans:
				link = ImageHandler.makeBans(path, self.id, self.getType(depth))
			if depth in MindMap.bluePicks or depth in MindMap.redPicks:
				link = ImageHandler.makeDraft(path, self.id, self.getType(depth))

			if not node.emptyNest():
				file.write("<node BACKGROUND_COLOR=\""+ backColor +"\" HGAP=\"30\" ID=\"ID_"+ str(self.id) +"\" VSHIFT = \"10\" STYLE = \"bubble\">\n")
				file.write("<richcontent TYPE=\"NODE\"><html><body><img src=\""+link+"\" /></body></html></richcontent>\n")
				self.id = self.id + 1
				i = 0
				for child in node.getChildren():
					i += 1
					self.recurWrite(child, file, depth + 1, newPath[:])
				file.write("</node>\n")
			else:
				file.write("<node BACKGROUND_COLOR=\""+ backColor +"\" HGAP=\"30\" ID=\"ID_"+ str(self.id) +"\" VSHIFT = \"10\" STYLE = \"bubble\">\n")
				file.write("<richcontent TYPE=\"NODE\"><html><body><img src=\""+link+"\" /></body></html></richcontent></node>\n")
				self.id = self.id + 1
				return


	def generateMindMap(self, tree):
		file = open(self.outFile, "w")
		file.write("<map version=\"1.0.1\">\n")
		self.recurWrite(tree.getRoot(), file, 0, [])
		file.write("</map>\n")
		file.close()

	def getType(self, depth):
		# 0 - Blue Ban
		# 1 - Red Ban
		# 2 - Blue Draft
		# 3 - Red Draft
		if depth is 9 or depth is 17:
			return 3
		if depth is 10 or depth is 18:
			return 2
		if depth % 2 is 1:
			if depth <= 6 or (depth >= 13 and depth <= 16):
				return 0
			return 2
		if depth <= 6 or (depth >= 13 and depth <= 16):
			return 1
		return 3


class SimpleCSV:
	def __init__(self, name):
		self.topLim = 2
		self.botLim = 14 
		self.leftPoint = 4
		self.rightPoint = 24
		self.fileName = name

	def getDrafts(self):
		drafts = []
		with open(self.fileName, newline='') as csvFile:
			spamreader = csv.reader(csvFile, delimiter=',', quotechar='|')
			rowCount = 0
			for row in spamreader:
				tempDraft = []
				if rowCount >= self.topLim and rowCount <= self.botLim:
					colCount = 0
					for entry in row:
						if colCount is not 19 and colCount >= self.leftPoint and colCount <= self.rightPoint:
							tempDraft.append(entry)
						colCount = colCount+1
					drafts.append(tempDraft)
				rowCount = rowCount+1
		return drafts


myCSV = SimpleCSV("test2.csv")
draftList = myCSV.getDrafts()

mainTree = Tree("VS SKT")
for draft in draftList:
	mainTree.addDraft(draft)

mainMap = MindMap("test1")
mainMap.generateMindMap(mainTree)