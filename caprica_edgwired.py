import sys
import nltk
import re
from nltk.corpus import wordnet
import random

chat = list()
# http://tartarus.org/~martin/PorterStemmer/

class Line:
	def __init__(self, i, a, l):
		self.id = i
		self.author = a
		self.words = l
		self.lookup = list()

	def expand_words(self):
		templookup = self.words.split(" ")

		for word in templookup:
			sense_list = wordnet.synsets(word)
			if sense_list:
				i = 0
				templist = list()
				for sense in sense_list:
					templist.extend(sense_list[i].lemma_names)

					i += 1
				self.lookup.append(templist)
			else:
				self.lookup.append([word])
			
# query_line = Line(1,"eric","meaning of life")
# query_line.expand_words()
# 
# print query_line.lookup



#query_line = Line(1,"eric","hello michael how are things")
#query_line = Line(1, "michael","i am not in love with this corpus")


file = open("/Users/voxels/Documents/ITP/02/Learning Bit by Bit/Caprica Project/Caprica/edgwired_clean.txt")
text = file.readlines()



for row in text:
	row = row.strip()
	parseString = row.split(',',3)

	conversation_id = parseString[0]
	time = parseString[1]
	author = parseString[2]
	words = parseString[3]

	chat.append(Line(conversation_id, author, words))
	



# This is crude. It gives the line of some other's text
# with the most instances of the synonyms in our query string
def ask_something(you_ask):
	
	query_line = Line(1,"eric", you_ask)
	query_line.expand_words()

	row_index = 0
	best_fit = 0
	best_index = 0
	
	for chat_line in chat:
	
		if "Edgwired" not in chat_line.author:
	
			fit = 0
	
			for synonyms in query_line.lookup:
				for word in synonyms:
					if word in chat_line.words:
						fit += 1
			#print "line " + str(row_index) + " has fit of " + str(fit)
			# change to a >= to give us older michael
			# this is a problem, if we have a bunch of matches
			# we need some kind of round 2 filter to pick the
			# very best one and break the tie
			if fit > best_fit:
				# uncomment to print top candidates
				# print "Score: " + str(fit) + " " + chat_line.author + ": " + chat_line.words		
				best_index = row_index
				best_fit = fit
				
		row_index += 1

	#print best_fit
	#print chat[best_index].words

	# Now let's start at the chat line that best fit our query string,
	# and then walk forward through the log to Michael's response

	# also need to factor chat boundaries
	for chat_line in chat[best_index:len(chat)]:
		
		print chat_line.author + ": " + chat_line.words		
		if "Edgwired" in chat_line.author:
			break

		


# print ask_something("meaning of life");

while 1:

	you_say = raw_input("You say: ")
	
	if you_say == "quit":
		break
	else:
		print ask_something(you_say)
	

##print len(chat)
##print chat[-1].author
##print chat[-1].words
