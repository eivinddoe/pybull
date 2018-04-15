import csv

def loadData():
	with open('data.csv', 'r') as f:
		reader = csv.reader(f)
		data = list(reader)
	return(data)
