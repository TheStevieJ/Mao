topLim = 2
botLim = 124
leftPoint = 9
rightPoint = 39

import csv

drafts = []

with open("testIn.csv", newline='') as csvFile:
	spamreader = csv.reader(csvFile, delimiter=',', quotechar='|')
	rowCount = 0
	for row in spamreader:
		tempDraft = []
		if rowCount >= topLim and rowCount <= botLim:
			colCount = 0
			for entry in row:
				if colCount is not 19 and colCount >= leftPoint and colCount <= rightPoint:
					tempDraft.append(entry)
				colCount = colCount+1
			drafts.append(tempDraft)
		rowCount = rowCount+1
print (drafts)

