# Feb 23, 2019

# gee.py

# Project 2: Gee Parser.

#

# The program parse the input according to the gee grammar and product the abstract syntax trees.

#

# This file is supposed to serve as a reference when you work on Project 3. Thanks to all students, whose codes are great examples to learn from.



import re, sys, string



debug = False

dict = { }

tokens = [ ]



# Class of StatementList: maintain a list of Statement objects

class StatementList( object ):

	def __init__(self):

		self.statementList = []



	def addStatement(self, statement):

		self.statementList.append(statement)



	def __str__(self):

		printStr = ''

		for statement in self.statementList:

			printStr += str(statement)

		return printStr

	def meaning(self, state):
		for section in self.statementList:

			section.meaning(state)

		return state



# === Statement class and subclasses

class Statement( object ):

	def __str__(self):

		return ""



class Assignment( Statement ):

	def __init__(self, identifier, expression):

		self.identifier = identifier

		self.expression = expression



	def __str__(self):

		return "= " + str(self.identifier) + " " + str(self.expression) + "\n"

	def meaning(self, state):
		#print("hereeee")
		#print(state)
		#print(self.identifier)
		#print(self.expression)
		#print(self.expression.value(state))
		state[self.identifier] = self.expression.meaning(state)
		#print(state)
		return state


class WhileStatement( Statement ):
	def __init__(self, expression, block):

		self.expression = expression

		self.block = block



	def __str__(self):

		return "while " + str(self.expression) + "\n" + str(self.block) + "endwhile\n"

	def meaning(self, state):
		while self.expression.meaning(state) == True:

			self.block.meaning(state)

		return state




class IfStatement( Statement ):

	def __init__(self, expression, ifBlock, elseBlock):

		self.expression = expression

		self.ifBlock = ifBlock

		self.elseBlock = elseBlock



	def __str__(self):

		return "if " + str(self.expression) + "\n" + str(self.ifBlock) + "else\n" + str(self.elseBlock) + "endif\n"

	def meaning(self, state):
		#print(self.expression.value(state))
		if self.expression.meaning(state) == True:
			#print(self.ifBlock)
			self.ifBlock.meaning(state)
			#print("here")
			return state
		elif self.elseBlock is not '':

			self.elseBlock.meaning(state)
			
			return state
		
		return state


# === Expression class and subclasses

class Expression( object ):

	def __str__(self):

		return ""



class BinaryExpr( Expression ):

	def __init__(self, op, left, right):

		self.op = op

		self.left = left

		self.right = right



	def __str__(self):

		return str(self.op) + " " + str(self.left) + " " + str(self.right)

	def meaning(self,state):
		#print("hereee")
		left = self.left.meaning(state)
		right = self.right.meaning(state)
		if self.op == '+':
			return left + right # not sure if the plus should be a string or the operation
		elif self.op == '-':
			return left - right
		elif self.op == '*':
			return left * right
		elif self.op == '/':
			return left / right
		elif re.match(Lexer.relational, self.op):
			switcher = {
			">": left > right,
			"<": left < right,
			">=": left >= right,
			"<=:": left <= right, 
			"==": left == right,
			"!=": left != right,
			}
			#print("here:", switcher.get(self.op))
			return switcher.get(self.op, "invalid realtion")
		elif self.op in ["and", "or"]:
			switcher = {
			"and": left and right,
			"or": left or right
			}
			return switcher.get(self.op, "invalid relation")

class Number( Expression ):

	def __init__(self, value):

		self.number = int(value)


	def __str__(self):

		return str(self.number)

	def meaning(self, state):
		return int(self.number)


class VarRef( Expression ):

	def __init__(self, value):

		self.relation = value



	def __str__(self):

		return str(self.relation)

	def meaning(self, state):

		return state[self.relation]




class String( Expression ):

	def __init__(self, value):

		self.string = value



	def __str__(self):

		return str(self.string)

	def meaning(self):
		return self.string


# Lexer, a private class that represents lists of tokens from a Gee

# statement. This class provides the following to its clients:

#

#   o A constructor that takes a string representing a statement

#       as its only parameter, and that initializes a sequence with

#       the tokens from that string.

#

#   o peek, a parameterless message that returns the next token

#       from a token sequence. This returns the token as a string.

#       If there are no more tokens in the sequence, this message

#       returns None.

#

#   o removeToken, a parameterless message that removes the next

#       token from a token sequence.

#

#   o __str__, a parameterless message that returns a string representation

#       of a token sequence, so that token sequences can print nicely



class Lexer :





	# The constructor with some regular expressions that define Gee's lexical rules.

	# The constructor uses these expressions to split the input expression into

	# a list of substrings that match Gee tokens, and saves that list to be

	# doled out in response to future "peek" messages. The position in the

	# list at which to dole next is also saved for "nextToken" to use.



	special = r"\(|\)|\[|\]|,|:|;|@|~|;|\$"

	relational = "<=?|>=?|==?|!="

	arithmetic = "\+|\-|\*|/"

	#char = r"'."

	string = r"'[^']*'" + "|" + r'"[^"]*"'

	number = r"\-?\d+(?:\.\d+)?"

	literal = string + "|" + number

	#idStart = r"a-zA-Z"

	#idChar = idStart + r"0-9"

	#identifier = "[" + idStart + "][" + idChar + "]*"

	identifier = "[a-zA-Z]\w*"

	lexRules = literal + "|" + special + "|" + relational + "|" + arithmetic + "|" + identifier



	def __init__( self, text ) :

		self.tokens = re.findall( Lexer.lexRules, text )

		self.position = 0

		self.indent = [ 0 ]





	# The peek method. This just returns the token at the current position in the

	# list, or None if the current position is past the end of the list.



	def peek( self ) :

		if self.position < len(self.tokens) :

			return self.tokens[ self.position ]

		else :

			return None





	# The removeToken method. All this has to do is increment the token sequence's

	# position counter.



	def next( self ) :

		self.position = self.position + 1

		return self.peek( )





	# An "__str__" method, so that token sequences print in a useful form.



	def __str__( self ) :

		return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"







# The "parse" function. This builds a list of tokens from the input string,

# and then hands it to a recursive descent parser for the PAL grammar.

# This is where the work is started after the tokens are loaded in correctly.



def parse( text ) :

	global tokens

	tokens = Lexer( text )

	stmtlist = parseStmtList( )

	#print (stmtlist)

	return stmtlist

def state(stateList):
	state_dict = {}
	state_dict = stateList.meaning(state_dict)
	#print("state_dict", state_dict)
	semantics_final = semantic_format(state_dict)
	print(semantics_final)
	return

def semantic_format(statedict):
	#print(stateList)
	final = ""
	for k, v in statedict.items():
		final += " ,<" + str(k) + ", " + str(v) + ">"
		#print(final)
	final = final[2:]
	return "{" + final + "}"




def parseStmtList(  ):

	""" stmtList =  {  statement  } """



	tok = tokens.peek( )

	statementList = StatementList()



	while tok not in [None ,"~"]: #have to account for undent that signals an end of block



		statement = parseStatement()

		statementList.addStatement(statement)

		tok = tokens.peek()



	return statementList





def parseStatement():

	"""statement = ifStatement |  whileStatement  |  assignment"""



	tok = tokens.peek()

	if debug: print ("Statement: ", tok)



	if tok == "if":

		return parseIfStmt()



	elif tok == "while":

		return parseWhileStmt()



	elif re.match(Lexer.identifier, tok):

		return parseAssignment()



	error("error msg: statement")

	return





def parseAssignment():

	"""assign = ident "=" expression  eoln"""



	identifier = tokens.peek()

	if debug: print ("Assign statement: ", left)



	if tokens.next() != "=":

		error("error msg: assignment")



	tokens.next()

	exp = expression()



	tok = tokens.peek()

	if tok != ";":

		error("error msg: assignment")



	tokens.next()



	return Assignment(identifier, exp)







def parseIfStmt():

	"""ifStatement = "if" expression block   [ "else" block ] """

	tok = tokens.next()

	if debug: print ("If statement: ", tok)

	expr = expression()

	ifBlock = parseBlock()

	elseBlock = ''

	if tokens.peek() == "else":

		tok = tokens.next()

		if debug: print ("Else statement: ", tok)

		elseBlock = parseBlock()

	return IfStatement(expr, ifBlock, elseBlock)





def parseWhileStmt():

	"""whileStatement = "while"  expression  block"""

	tok = tokens.next()

	if debug: print ("While statement: ", tok)

	expr = expression()

	block = parseBlock()

	return WhileStatement(expr, block)





def parseBlock():

	"""block = ":" eoln indent stmtList undent"""

	tok = tokens.peek()

	if debug: print ("Block: ", tok)

	# Check to make sure each of the appropriate terminal tokens exist and are in the right place

	if tok != ":":

		error("error msg: block")

	tok = tokens.next()

	if tok != ";":

		error("error msg: block")

	tok = tokens.next()

	if tok != "@":

		error("error msg: block")

	tok = tokens.next()

	stmtList = parseStmtList()



	if tokens.peek() != "~":

		error("error msg: block")



	tokens.next()



	return stmtList





def expression():

	"""expression = andExpr { "or" andExpr }"""

	tok = tokens.peek( )

	if debug: print ("expression: ", tok)

	left = andExpr( )

	tok = tokens.peek( )

	while tok == "or":

		tokens.next()

		right = andExpr( )

		left = BinaryExpr(tok, left, right)

		tok = tokens.peek( )

	return left





def andExpr():

	"""andExpr    = relationalExpr { "and" relationalExpr }"""



	tok = tokens.peek( )

	if debug: print ("andExpr: ", tok)

	left = relationalExpr( )

	tok = tokens.peek( )

	while tok == "and":

		tokens.next()

		right = relationalExpr( )

		left = BinaryExpr(tok, left, right)

		tok = tokens.peek( )

	return left





def relationalExpr():

	"""relationalExpr = addExpr [ relation addExpr ]"""



	tok = tokens.peek( )

	if debug: print ("relationalExpr: ", tok)

	left = addExpr( )

	tok = tokens.peek( )

	while re.match(Lexer.relational, tok):

		tokens.next()

		right = addExpr( )

		left = BinaryExpr(tok, left, right)

		tok = tokens.peek( )

	return left





def addExpr( ):

	""" addExpr    = term { ('+' | '-') term } """



	tok = tokens.peek( )

	if debug: print ("addExpr: ", tok)

	left = term( )

	tok = tokens.peek( )

	while tok == "+" or tok == "-":

		tokens.next()

		right = term( )

		left = BinaryExpr(tok, left, right)

		tok = tokens.peek( )

	return left







def term( ):

	""" term    = factor { ('*' | '/') factor } """



	tok = tokens.peek( )

	if debug: print ("Term: ", tok)

	left = factor( )

	tok = tokens.peek( )

	while tok == "*" or tok == "/":

		tokens.next()

		right = factor( )

		left = BinaryExpr(tok, left, right)

		tok = tokens.peek( )

	return left





def factor( ):

	"""factor  = number | string | ident |  "(" expression ")" """



	tok = tokens.peek( )



	if debug: print ("Factor: ", tok)



	if re.match(Lexer.number, tok):

		expr = Number(tok)

		tokens.next( )

		return expr



	elif re.match(Lexer.string, tok):

		expr = String(tok)

		tokens.next()

		return expr



	elif re.match(Lexer.identifier, tok):

		expr = VarRef(tok)

		tokens.next()

		return expr



	if tok == "(":

		tokens.next( )  # or match( tok )

		expr = expression( )

		tokens.peek( )

		tok = match(")")

		return expr



	error("error msg: factor()")

	return





def match(matchtok):

	tok = tokens.peek( )

	if (tok != matchtok): error("error msg: match()")

	tokens.next( )

	return tok



def error( msg ):

	sys.exit(msg)







def mklines(filename):

	inn = open(filename, "r")

	lines = [ ]

	pos = [0]

	ct = 0

	file = ""

	for line in inn:
		file += line
		ct += 1

		line = line.rstrip( )+";"

		line = delComment(line)

		if len(line) == 0 or line == ";": continue

		indent = chkIndent(line)

		line = line.lstrip( )

		if indent > pos[-1]:

			pos.append(indent)

			line = '@' + line

		elif indent < pos[-1]:

			while indent < pos[-1]:

				del(pos[-1])

				line = '~' + line

		#print (ct, "\t", line)

		lines.append(line)

	# print len(pos)

	undent = ""
	print(file)

	for i in pos[1:]:

		undent += "~"

	lines.append(undent)

	inn.close()



	return lines





def chkIndent(line):

	ct = 0

	for ch in line:

		if ch != " ": return ct

		ct += 1

	return ct





def delComment(line):

	pos = line.find("#")

	if pos > -1:

		line = line[0:pos]

		line = line.rstrip()

	return line







def main():



	global debug

	ct = 0

	for opt in sys.argv[1:]:

		if opt[0] != "-": break

		ct = ct + 1

		if opt == "-d": debug = True

	if len(sys.argv) < 2+ct:

		print ("Usage:  %s filename" % sys.argv[0])

		return

	original = parse("".join(mklines(sys.argv[1+ct])))
	state(original)

	return





main()

