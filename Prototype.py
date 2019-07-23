import csv
import requests
import PIL
import tkinter as tk
from PIL import Image
from io import BytesIO
from tkinter import filedialog

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
			if name is "":
				outNames.append("Empty")
			else:
				tempName = name.replace("\'", " ").title()
				tempName = tempName.replace(" ","")
				outNames.append(tempName)
		return outNames
		
	def makeNewDraft(names, id, num):
		order = [[[0,2,4,12,14],[1,3,5,13,15]],[[6,9,10,17,18],[7,8,11,16,19]]]
		names = ImageHandler.formatNames(names)
		for name in names:
			ImageHandler.loadImage(name)
		picks = len(names)
		for x in range(picks, 21):
			names.append("Empty")
		fileNames = []
		for name in names:
			fileNames.append("Images/"+ name + ".png")
		images = map(Image.open, fileNames)
		new_im = Image.new('RGB', (660, 150))
		yOffset = 0
		for group in order:
			xOffset = 0	
			for row in group:
				for img in row:
					tempImg = Image.open(fileNames[img])
					new_im.paste(tempImg.resize((60,60), PIL.Image.ANTIALIAS), (xOffset, yOffset))
					xOffset += 60
				xOffset += 60
			yOffset += 90
		location = "Images/"+str(id)+".png"
		new_im.save(location)
		return location


class Pick:
	def __init__(self, name):
		self.name = name
		self.children = []

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
			if champ is "":
				return
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
				link = ImageHandler.makeNewDraft(path, self.id, self.getType(depth))
			if depth in MindMap.bluePicks or depth in MindMap.redPicks:
				link = ImageHandler.makeNewDraft(path, self.id, self.getType(depth))

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
		self.leftPoint = 3
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
						if colCount >= self.leftPoint and colCount <= self.rightPoint:
							tempDraft.append(entry)
						colCount = colCount+1
					drafts.append(tempDraft)
				rowCount = rowCount+1
		for draft in drafts:
			if draft[0] is "":
				drafts.remove(draft)

		return drafts


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Load File\n(click me)"
		self.hi_there["command"] = self.say_hi
		self.hi_there.pack(side="top")
		self.create_doc = tk.Button(self)
		self.create_doc["text"] = "Load File First"
		self.create_doc["command"] = self.errorPrint
		self.create_doc.pack(side="top")
		self.quit = tk.Button(self, text="QUIT", fg="red",
								command=self.master.destroy)
		self.quit.pack(side="bottom")

	def say_hi(self):
		self.filename = filedialog.askopenfilename(initialdir = "/",
													title = "Select draft file",
													filetypes = (("CSV Draft","*.csv"),("all files","*.*"))
													)
		self.hi_there["text"] = "File Found"
		self.create_doc["text"] = "File Loaded\n(click me)"
		self.create_doc["command"] = self.parse
		print(self.filename)

	def errorPrint(self):
		print("No file loaded")

	def parse(self):
		myCSV = SimpleCSV(self.filename)
		draftList = myCSV.getDrafts()

		mainTree = Tree("HEAD")
		for draft in draftList:
			mainTree.addDraft(draft)

		mainMap = MindMap("test1")
		mainMap.generateMindMap(mainTree)
		self.create_doc["text"] = "File Created!"


root = tk.Tk()
app = Application(master=root)
app.mainloop()