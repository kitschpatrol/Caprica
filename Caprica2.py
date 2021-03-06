##Back to the Future IM Module
##Eric Mika + Michael Edgcumbe
##Learning Bit by Bit at NYU ITP, Spring 2010

## Suggested Improvements:

##synonym/ DONE
##n-gram/	 DONE
##question+response
##flagged
##original word/
##length of response/
##porter stemming/
##variations/
##dictionary/


import sys
import nltk
import re
from nltk.corpus import wordnet
from nltk import pos_tag
##from nltk.corpus import brown
##from nltk.corpus import nps_chat
from nltk.collocations import *
import random

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

## CREATE A CLASS TO HOLD THE IM DATA
class Line:
	## class holds the chat data, lookup is a list of synonyms	 
	def __init__(self,i,a,l,d):
		self.id = i
		self.author = a
		self.words = l
		self.lookup = list()
		self.index = d
		self.ngrams = list()
		self.synonymScore = 0
		self.used = 0

def lowerStrings(word_list):
	return [x.lower() for x in word_list]


def expand_words(words):
	## tokenize the list of words
	templookup = words.split(" ")
	
	lookup = list()
	uniqueLookup = list()
	
	for word in templookup:
		## for each word in the split list, create a new list which holds the synonyms
		sense_list = wordnet.synsets(word)
		
		if sense_list:
			i = 0
			templist = list()
			for sense in sense_list:
				# force lowercase
				templist.extend(lowerStrings(sense_list[i].lemma_names))
				i+=1
			## append the synonyms to the lookup list of words for the sentence
			lookup.append(templist)
		else:
			## if there are no synonyms, append the word used as the search term
			lookup.append([word])
	
	# remove duplicates
	for synonyms in lookup:
		uniqueLookup.append([x for x in synonyms if x not in locals()['_[1]']])
	
	return uniqueLookup






## READ IN AND STORE THE IM TEXT
file = open("edgwired_clean_chunked.txt")
rawEdg = file.readlines()

file = open("../obrigado_clean_chunked.txt")
rawMika = file.readlines()

##file = open("allwords.txt")
##allwords = file.read()

## create a new list to hold the chat data
edgwired = list()
obrigado = list()


## PARSE THE DATA
def masticator(rawlog):
	digestedlist = list()
	index = 0
	for row in rawlog:
		## remove the \n
		row = row.strip()
		## split on the first 3 commas
		parseString = row.split(',',3)

		## store in variables and append to the chat list
		conversation_id = parseString[0]
		time = parseString[1]
		author = parseString[2]
		words = parseString[3]

		digestedlist.append(Line(conversation_id,author,words, index))
		index += 1

	return digestedlist


## SEARCH THE DATA
def search(query, bank):
				hits = list()
				print query.lookup
				synonymLimit = 3 # max number of synonyms to consider

				#Find the matches between synonyms
				for line in bank:
						for synonyms in query.lookup:
								for synonym in synonyms[0:synonymLimit]:
										if synonym in line.words:
												# found a match, bump the score
												line.synonymScore += 1
												
												# bonus score if it's the original word
												if synonyms[0] == synonym:
													line.synonymScore += 2
												
												# add it to the hit list if we need to
												# this means we don't need to find unique later
												if line not in hits:
													hits.append(line)
													
						# if line.synonymScore > 0:
						# 	print line.synonymScore
						# 	# print line.words
							
				print len(hits)
				print "done"
				return hits

def synonym_search(query, log):
	hits = list()
	best_score = 0
	best_index = 0
	
	for line in log:
		for synonyms in query.lookup:
			for word in synonyms[0:4]:
				if word in line.words:
					line.synonymScore += 1

		if line.synonymScore > best_score:
			best_score = line.synonymScore

	print best_score
	
	# now we have the best score
	for line in log:
		for synonyms in query.lookup:
			for word in synonyms[0:4]:
				if word in line.words:
					line.synonymScore += 1

		if line.synonymScore =- best_score:
			hits.append(line)
	
	
	
	print hits
						


##RANK THE MATCHES
def rank(current_speaker, query, possibilities):

		bigram_list = list()
		
		for message in possibilities:
				bigram_list.append(BigramCollocationFinder.from_words(message.words))

		for bigram in bigram_list:
				print bigram.nbest(bigram_measures.likelihood_ratio,10)

##		sorted(bigram_list
##
##					 bigram_finder.nbest(bigram_measures.raw_freq,10))

##bigram_finder = BigramCollocationFinder.from_words(allwords_tokens)
##bigram_scored = bigram_finder.score_ngrams(bigram_measures.raw_freq)
##
##trigram_finder = TrigramCollocationFinder.from_words(allwords_tokens)
##trigram_scored = trigram_finder.score_ngrams(trigram_measures.raw_freq)

## SORT: sorted(bigram_finder.nbest(bigram_measures.raw_freq,10)
## FILTER BY FREQUENCY: bigram_finder.apply_freq_filter(5)
## FIND LENGTH: len(bigram_finder.score_ngrams(bigram_measures.raw_freq))
						




edgwired = masticator(rawEdg)
#obrigado = masticator(rawMika)

i_say = "that is strange"
#i_say = sys.argv[1]
my_name = "obrigado"
prime_query = Line(0,my_name,i_say,0)
prime_query.lookup = expand_words(prime_query.words)

query = prime_query
possibilities = synonym_search(prime_query,edgwired)	 #returns a list of line objects that have matched words or synonyms


#print len(possibilities)
#rank("Obrigado",i_say,possibilities)


if "obrigado" in my_name:
		my_name = "edgwired"
else:
		my_name = "obrigado"




#### CREATE BIGRAMS AND TRIGRAMS
##allwords_tokens = nltk.wordpunct_tokenize(allwords)
##
##bigram_finder = BigramCollocationFinder.from_words(allwords_tokens)
##bigram_scored = bigram_finder.score_ngrams(bigram_measures.raw_freq)
##
##trigram_finder = TrigramCollocationFinder.from_words(allwords_tokens)
##trigram_scored = trigram_finder.score_ngrams(trigram_measures.raw_freq)

## SORT: sorted(bigram_finder.nbest(bigram_measures.raw_freq,10)
## FILTER BY FREQUENCY: bigram_finder.apply_freq_filter(5)
## FIND LENGTH: len(bigram_finder.score_ngrams(bigram_measures.raw_freq))


##TAGGING
#nps_train = nltk.corpus.nps_chat.tagged_words('10-19-20s_706posts.xml')
#unigram_tagger = nltk.UnigramTagger(nps_train)
#bigram_tagger = nltk.BigramTagger(nps_train, backoff=unigram_tagger)

#brown_news_tagged = brown.tagged_sents(categories = 'news')
#tagger = nltk.UnigramTagger(brown_news_tagged)
