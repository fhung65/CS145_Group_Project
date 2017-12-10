import sys
import csv
import os
import pickle
import re

stopWords = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}
RE_D = re.compile('\d')

def generateClusterTable(hashTableFilename):
	hashTable = {}
	cache = {}
	curr = ""
	with open(hashTableFilename, 'r') as inFile:
		for line in inFile:
			line = line.split()
			if line[0] != curr and curr != "":
				curr = line[0]
				maxWord = max(cache, key = cache.get)
				for word in cache:
					hashTable[word] = maxWord
	return hashTable

def sanitize(dataStr, clusterHashTable):
	outputWords = []
	words = dataStr.split()
	for word in words:
		if word in clusterHashTable:
			word = clusterHashTable[word]
		if word not in stopWords and not RE_D.search(word):
			outputWords.append(word)
	return ' '.join(outputWords)


def main():
    if len(sys.argv) != 3:
    	print("Need csv input and output filenames as arguments")
    clusterTableFilename = "cmu_cluster.txt"
    clusterHashTableFilename = "cluster.pickle"
    if os.path.isfile(clusterHashTableFilename):
    	clusterTable = pickle.load(clusterHashTableFilename)
    else:
    	clusterTable = generateClusterTable(clusterTableFilename)
    inputCSV = sys.argv[1]
    outputCSV = sys.argv[2]
    with open(inputCSV, "r") as inFile, open(outputCSV, 'w') as outFile:
    	reader = csv.reader(inFile)
    	writer = csv.writer(outFile)
    	for line in reader:
    		writer.writerow([sanitize(line[0], clusterTable), line[1]])

if __name__ == "__main__":
	main()