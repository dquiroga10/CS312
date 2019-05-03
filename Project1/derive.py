#! /usr/bin/python3

# Author: Daniel Quiroga

import string
from queue import *

length = int(input("Length? "))

filename = input("Filename? ")

pod = {} # dictionary that will be used to keep track of the grammar
sym = None # reference to the start symbol 
pro = [] # reference to the rhs of the start symbol
worklist = Queue() # what will be used to derive all the possible outcomes to the grammar
printed = [] # will keep track of what is already printed and avoid printing duplicates -- mainly for ambiguous grammar


for line in open(filename, "r"): # reads file 
	words = line.split()
	words.remove("=")
	rhs = words[1:]
	if words[0] in pod.keys():
		pod[words[0]].append(rhs) # adding to an existing key in the dictionary
	elif words[0] not in pod.keys(): 
		pod[words[0]] = [rhs] # creating a new key and adding the rhs to it 
		if sym == None:
			sym = words[0] # keeping track of the start symbol and its rhs 
			pro = rhs


def stackAlgo(wl):
	while wl.empty() == False:

		s = wl.get()

		wl = pop(s, wl)

def pop(sentence, wl): 
	sentence = sentence.split()
	size = len(sentence)

	if size <= length:
		for i in range(0, size): #going through each part of the s and seeing if there is a non terminal
			if sentence[i] in pod.keys():
				rhsSize = len(pod.get(sentence[i])) # gets how many objects are on the rhs of the key 
				rhs = pod.get(sentence[i]) # gets a reference to the objects 
				for j in range(0, rhsSize): # iterate through objects on rhs to get rid of the brackets and only have characters (easier to work with characters than lists)
					tmp = ""
					tmpS = len(rhs[j])
					if i > 0:
						for m in range(0, i):
							tmp += sentence[m] + " "
					for k in range(0,tmpS):
						tmp += str(rhs[j][k]) + " "
					if i < size:
						for n in range(i + 1, size):
							tmp +=  " " + sentence[n]
					wl.put(tmp.strip()) # this will take out all the extra white space at the end and then place it in the queue, using replace we take out any extra white space in the middle
				return wl # this will return the worklist the added objects to it now
		else: # gets here if the for loop does not find a non terminal 
			pri = ""
			for s in range(0, size):
				pri += sentence[s] + " " # prints out terminal correctly with one space
			if pri not in printed: # checking if the derivation has been printed yet
				printed.append(pri)
				print(pri)
			return wl # always return the worklist to continue the algorithm
	else:
		return wl # if the s is greater than the length then it is just disregarded

worklist.put(sym)
stackAlgo(worklist)