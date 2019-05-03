#! /usr/bin/python3

# Daniel Quiroga 
# March 11, 2019

# Project 4: type.py
""" semantics.py implements a dynamically typed version of a subset of Gee.
This subset makes sure that all variables are first defined with a specific
type and then makes sure that only operations valid for that type are performed"""





import re, sys, string



debug = False

dict = { }

tokens = [ ]

math = ["+", "-", "*", "/"]

bools = ['>','<','<=','>=','==','!=','and','or']


# Class of StatementList: maintain a list of Statement objects



class StatementList( object ):

	def __init__(self):

		self.statementList = [ ]



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

	def tipe(self, tm):
		
		for section in self.statementList:

			section.tipe(tm)
		
		#return tm #used for debugging





# Statement class and subclasses



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

		state[self.identifier] = self.expression.meaning(state)

		return state

	def tipe(self, tm):
		tipe_return = self.expression.tipe(tm)
#make sure something is returned this will also be caught later on as well -- wrote it when i started the project
		if tipe_return == "":

			error("Type Error: variable is never defined!")
# this will make sure that the current variable has not be defined yet and will now have a type associated to it 
		if self.identifier not in tm:

			tm[self.identifier] = tipe_return

			type_print(self.identifier, tipe_return) #the actual printing mechanism
		else: 

			if tm[self.identifier] != tipe_return: #check to see if it matches the tipes if not return an error

				error("Type Error: " + str(tm[self.identifier]) + " = " + str(tipe_return) + "!")




class WhileStatement( Statement ):

	def __init__(self, expression, block):

		self.expression = expression

		self.block = block



	def __str__(self):

		return "while " + str(self.expression) + "\n" + str(self.block) + "endwhile\n"



	def meaning(self, state):

        #checks if the value of the expression exists, then obtains the value of the block
		while self.expression.meaning(state) == True:

			self.block.meaning(state)

		return state

	def tipe(self, tm):

		tipe_return = self.expression.tipe(tm)
		#in while loops we need the expression to contain a boolean or else the while statement will never enter
		if tipe_return != "boolean":

			error("Type Error: While statement does not contain a boolean expression.")

		#then i just take the block and run it through the type checker to make sure everything is defined and performed properly
		self.block.tipe(tm)

		#return tm



class IfStatement( Statement ):

	def __init__(self, expression, ifBlock, elseBlock):

		self.expression = expression

		self.ifBlock = ifBlock

		self.elseBlock = elseBlock



	def __str__(self):

		return "if " + str(self.expression) + "\n" + str(self.ifBlock) + "else\n" + str(self.elseBlock) + "endif\n"



	def meaning(self, state):

        #checks if the value of the expression exists, then obtains the value of the ifBlock
		if self.expression.meaning(state) == True:

			self.ifBlock.meaning(state)

			return state


        #else: checks if the next block is not empty, then obtains the value of the elseBlock
		elif self.elseBlock is not '':

			self.elseBlock.meaning(state)

			return state

		return state

	def tipe(self, tm):
		tipe_return = self.expression.tipe(tm)

#in for loops we need the expression to contain a boolean or else the while statement will never enter
		if tipe_return != "boolean":

			error("Type Error: If statement does not contain a boolean expression.")

#then i just take the block and run it through the type checker to make sure everything is defined and performed properly
		self.ifBlock.tipe(tm)
#this just checks to see that the elseblock is not empty
		if not(self.elseBlock == ""): 

			self.elseBlock.tipe(tm)
		#return tm

# Expression class and subclasses



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

        #obtains left and right expressions
		left = self.left.meaning(state)

		right = self.right.meaning(state)


        #returns operations on left and right
		if self.op == '+':

			return left + right
		elif self.op == '-':

			return left - right

		elif self.op == '*':

			return left * right

		elif self.op == '/':

			return left / right


        #evaulates relationals for left and right expressions
		elif re.match(Lexer.relational, self.op):

			switcher = {

			">": left > right,

			"<": left < right,

			">=": left >= right,

			"<=:": left <= right,

			"==": left == right,

			"!=": left != right,

			}

			return switcher.get(self.op, "invalid relation")


        #evaluates and & or for left and right expressions
		elif self.op in ["and", "or"]:

			switcher = {

			"and": left and right,

			"or": left or right

			}

			return switcher.get(self.op, "invalid relation")

	def tipe(self, tm):
# this gets the types of both sides of the operation occuring (either boolean operator or math operator)
		right = self.right.tipe(tm)

		left = self.left.tipe(tm)
#if they do not match then this is an error
		if left != right:

			error("Type Error: Operation not possible between two different types.")
#then we just return if the expression is a number or a boolean
		if self.op in bools:#if self.op in bools and left == "boolean" and right == "boolean":

			return "boolean"

		elif self.op in math and left == "number" and right == "number": #elif self.op in math: 

			return "number"



class Number( Expression ):

	def __init__(self, value):

		self.number = int(value)



	def __str__(self):

		return str(self.number)



	def meaning(self, state):

        #gets integer value of a number
        #incase its written as a string
		return int(self.number)
#return that the variable is a number type
	def tipe(self, tm):

		return "number"





class VarRef( Expression ):

	def __init__(self, value):

		self.relation = value



	def __str__(self):

		return str(self.relation)



	def meaning(self, state):

        #returns relation as a key in state dictionary
		return state[self.relation]

	def tipe(self, tm):
		#bring up an error if the variable is never defined
		if self.relation not in tm: #not ( self. val in tm):

			error("Type Error: " + str(self.relation) + " is referenced before being defined!")
#this will just return the type of the variable
		return tm[self.relation]


# we do not need to worry about String in type checker 
class String( Expression ):

	def __init__(self, value):

		self.string = value



	def __str__(self):

		return str(self.string)



	def meaning(self):

        #returns the string
		return self.string



# Lexer, a private class that represents lists of tokens from a Gee



class Lexer :


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




	def peek( self ) :

		if self.position < len(self.tokens) :

			return self.tokens[ self.position ]

		else :

			return None



	def next( self ) :

		self.position = self.position + 1

		return self.peek( )



	def __str__( self ) :

		return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"








def parse( text ) :

	global tokens

	tokens = Lexer( text )

	stmtlist = parseStmtList( )

	return stmtlist



def state(stateList):
    """state function creates a dictionary for the state
    and calls meaning() and semantic_format() on it"""

    statedict = {} #state dictionary
    state_dict = stateList.meaning(statedict) #calls meaning on dictionary
    semantics_final = semantic_format(state_dict) #calls on semantic to format output
    print(semantics_final) #prints output
    return



def semantic_format(statedict):

    """semantic format function creates {<ident, state>} format for output"""

    final = "" #empty string
    for k, v in statedict.items(): #for each key and its value in state dictionary
        final += ", <" +str(k) + ", " + str(v) + ">" #add ", <key, value>" to string
    final = final[2:] #omits first space and comma
    return "{" + final +"}" #returns string with brackets

def types(stateList):

	typedict = {}
	stateList.tipe(typedict)
	# type_dict = stateList.tipe(typedict)
	# dictionary = types_dictionary(type_dict)
	# print(dictionary)



def types_dictionary(typedict):
	final = "" #empty string
	for k, v in typedict.items(): #for each key and its value in state dictionary
		final += ", <" +str(k) + ", " + str(v) + ">" #add ", <key, value>" to string
	final = final[2:] #omits first space and comma
	print("{" + final + "}")
	return "{" + final +"}" #returns string with brackets


def type_print(ident, tipe):
	if (ident is not "" and ident is not None) and (tipe is not "" and tipe is not None): 
		print(ident, tipe)
	else:
		error("Type Error: variable is never defined!")




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

	#print(file)

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

	#state(original)
	types(original)
 #calls state on parsed grammar
	return




main()

