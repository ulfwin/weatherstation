import csv

def getAll(filename):
	result = []
	with open(filename) as csvfile:
		reader = csv.reader(csvfile)
		# Remove first two rows
		reader.next()
		reader.next()
		for row in reader:
			if row[1] != '':
				result += [[float(row[0]),float(row[1])]]
	return result
