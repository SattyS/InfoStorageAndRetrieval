import os
import pickle
import re
import collections
import time
import math

def dd():
	return collections.defaultdict(int)

#data = {}
data = collections.defaultdict(dd)

def ddf():
	return collections.defaultdict(float)

#data = {}
dataFile = collections.defaultdict(ddf)
N = 0
start = time.time()
for root, dirs, files in os.walk("."):
	#Split root to contain the whole root as one entity in path
	path = root.split('/')
	#print "Directory Name ", os.path.basename(root)
	for file in files:
		#Check only .txt files, assuming other files don't have .txt in their filename
		if file.endswith(".txt"):
			N += 1
			fullPath = path[0] + '/' + file
			with open(fullPath) as f:
				#print "File Processing ...."
				#text = set()
				rows = f.read()
				#print "Rows ", rows
				words = [re.findall('[a-z0-9]+',rows.lower())]
				#print words
				for temp in words:
					for tempEle in temp:
						count = data[tempEle][file]
						data[tempEle][file] = count + 1
						#text.add(tempEle)
				#for tempKey in text:
					
		else:
			continue
end = time.time()
print "Boolean Index Build time - ", str(end - start)

start = time.time()
fileListFinal = []
for root, dirs, files in os.walk("."):
	#Split root to contain the whole root as one entity in path
	path = root.split('/')
	#print "Directory Name ", os.path.basename(root)
	for file in files:
		#Check only .txt files, assuming other files don't have .txt in their filename
		if file.endswith(".txt"):
			fullPath = path[0] + '/' + file
			fileListFinal.append(file)
			with open(fullPath) as f:
				#print "File Processing ...."
				#text = set()
				rows = f.read()
				#print "Rows ", rows
				words = [re.findall('[a-z0-9]+',rows.lower())]
				#print words
				for temp in words:
					for tempEle in temp:
						fileList = data[tempEle]
						idfd = len(fileList)
						idf = N / idfd
						idf = math.log10(idf)
						tf = data[tempEle][file]
						tf = 1 + math.log10(tf)
						dataFile[file][tempEle] = tf * idf
					
		else:
			continue
			
end = time.time()
print "Vector Index Build time - ", str(end - start)
print "End ."

#print data

while 1:
	
	query = raw_input("Enter a query: ")
	#print "Query ",query
	#print "Len ",len(query)
	if(len(query) <= 0):
		break;

	queryList = query.lower().split(' ')
	#print queryList
	queryResultList = []
	queryVector = collections.defaultdict(int)
	uniqueQueryList = []
	for tempQuery in queryList:
		queryResultList += data[tempQuery]
		if queryVector[tempQuery] == 0:
			uniqueQueryList.append(tempQuery) 
		queryVector[tempQuery] += 1
	#print queryResultList
	if len(queryList) is 1:
		print "Files in which the query is present ",queryResultList 
	else:
		rep = queryResultList[:]
		for i in set(queryResultList):
			rep.remove(i)    
		ans = []
		ans = set(rep)
		if not ans:
			print "Sorry no files found that match the query "
		else:
			print "Files in which the query is present ",ans
			
	
	# Cosine
	print "QV ", queryVector
	finalResult = collections.defaultdict(float)
	#print dataFile["a9983033.txt"]
	for f in fileListFinal:
		numerator = 0
		denominatorFinal = 1
		denominator = 0
		for tempUnique in uniqueQueryList:
			numerator += queryVector[tempUnique] * dataFile[f][tempUnique]
			denominator +=  queryVector[tempUnique] * queryVector[tempUnique]
		print "Num ", numerator
		print "Denom1 ", denominator
		tfidfVector = dataFile[f]
		print "tfidfVector ", tfidfVector
		denomSecTerm = 0
		for tfidf in tfidfVector:
			denomSecTerm += dataFile[f][tfidf] * dataFile[f][tfidf]
		print "DenomSec ", denomSecTerm
		denominatorFinal = math.sqrt(denominator) * math.sqrt(denomSecTerm)
		print "DenomFinal ", denominatorFinal
		finalResult[f] = numerator / denominatorFinal
		
	
	print finalResult
	
			
	
		
	
	
	

	



