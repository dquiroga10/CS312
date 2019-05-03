
import re, sys, string

debug = False
dict = { }
tokens = [ ]

#created by Daniel Quiroga 



#  Expression class and its subclasses
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

class Number( Expression ):
	def __init__(self, value):
		self.value = value
		
	def __str__(self):
		return str(self.value)

class VarRef( Expression ):
	def __init__(self, ident):
		self.ident = ident

	def __str__(self):
		return self.ident

class String( Expression ):
	def __init__(self, string):
		self.string = string

	def __str__(self):
		return str(self.string)

class StmtList( Expression ):
	def __init__(self, stmtList):
		self.stmtList = stmtList

	def __str__(self):
		return '\n'.join([str(line) for line in self.stmtList])

class Statement( object ):
	def __str__(self):
		return ""

class block( Statement ):
	def __init__(self, statement):
		self.statement = str(statement)

	def addStatement(self, next_statement):
		self.statement = str(self.statement) + "\n" + str(next_statement)

	def __str__(self):
		return self.statement

class whileStatement( Statement ):
	def __init__(self, whilestr, expression, block):
		self.expr = expression
		self.block = block

	def __str__(self):
		return 'while {}\n{}\nendwhile'.format(self.expr, self.block)

class ifStatement( Statement ):
	def __init__(self, expression, block, elseBlock = None):
		self.expression = expression
		self.block = block
		self.elseBlock = elseBlock

	def __str__(self):
		if self.elseBlock:
			return 'if {}\n{}\nelse\n{}\nendif'.format(self.expression, self.block, self.elseBlock)
		return 'if {}\n{}\nendif'.format(self.expression, self.block)

class assign( Statement ):
	def __init__(self, equals, identifier, expression):
		self.ident = identifier
		self.expr = expression
		
	def __str__(self):
		return '= {} {}'.format(self.ident, self.expr)

def error( msg ):
	#print msg
	sys.exit(msg)

# The "parse" function. This builds a list of tokens from the input string,
# and then hands it to a recursive descent parser for the PAL grammar.

def match( matchtok ):
	tok = tokens.peek( )
	if (tok != matchtok): error("Expecting "+ matchtok)
	tokens.next( )
	return tok

def expression( ):#DOUBLE CHECK THIS 
	"""expression 	 = andExpr { "or" andExpr } """
	
	tok = tokens.peek( )
	if debug: print("Expression: ", tok)
	left = andExpr( ) #does the left side of the grammar 
	tok = tokens.peek( )
	while tok == "or": #checks to see if there is the token or and will preform what is inside the curly bracket since it is a series 
		tokens.next()
		right = andExpr( )
		left = BinaryExpr(tok, left, right) # MIGHT HAVE TO CHANGE THIS TO STRING CAUSE ITS "or"
		tok = tokens.peek( )
	return left


def andExpr( ): #DOUBLE CHECK THIS 
	"""andExpr    = relationalExpr { "and" relationalExpr }"""

	tok = tokens.peek( )
	if debug: print("andExpr: ", tok)
	left = relationalExpr( ) #does the left side of the grammar
	tok = tokens.peek( )
	while tok == "and": #checks to see if there is the token "and" and will preform what is inside the curly bracket since it is a series 
		tokens.next()
		right = relationalExpr( )
		left = BinaryExpr(tok, left, right)#MIGHT HAVE TO CHANGE TO STRING 
		tok = tokens.peek( )
	return left 

relations    = ["==" , "!=" , "<" , "<=" , ">" , ">="] # used to see if there is a relation as the token 

def relationalExpr( ):#MAKE SURE I USED THE RIGHT LOGIC FOR THIS 
	"""relationalExpr = addExpr [ relation addExpr ]"""

	tok = tokens.peek( )
	if debug: print("relationalExpr: ", tok)
	left = addExpr( )
	expr = ""
	tok = tokens.peek( )
	if tok in relations:
		rel = relation( ) # expecting a relation to start off 
		right = expression( ) # if there is a relation we expect there to be an expression to the right of the relation
		expr = BinaryExpr( rel, left, right )
		return expr #fix this for syntax tree maybe

	return left

def relation( ):

	tok = tokens.peek( )
	if debug: print("relation: ", tok)
	expr = ""
	for i in relations:
		if tok == i:
			match( str(i) )#changed this a little to use VarRef
			expr = VarRef( tok )
			return expr
	error("Invalid relation")

def factor( ):
	"""factor     = number |  '(' expression ')' """

	tok = tokens.peek( )
	if debug: print ("Factor: ", tok)
	if re.match( Lexer.number, tok ):
		expr = Number(tok)
		tokens.next( )
		tok = tokens.peek( )
		return expr
	if tok == "(":
		tokens.next( )  # or match( tok )
		expr = addExpr( )#might need to change to expression( )
		tokens.peek( )
		tok = match( ")" )
		return expr
	if re.match( Lexer.identifier, tok ): # added this to take into accout identifiers
		expr = VarRef(tok)
		tokens.next( )
		return expr
	if re.match( Lexer.String, tok ): # added this to take into account strings
		expr = String( tok )
		return expr

	error( "Invalid operand" )
	return


def term( ):
	""" term    = factor { ('*' | '/') factor } """

	tok = tokens.peek( )
	if debug: print ("Term: ", tok)
	left = factor( )
	tok = tokens.peek( )
	while tok == "*" or tok == "/":
		tokens.next()
		right = factor( )
		left = BinaryExpr( tok, left, right )
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
		left = BinaryExpr( tok, left, right )
		tok = tokens.peek( )
	return left

def parseBlock( ): # parse routine for block that uses the block class to print out the appropriate string of the syntax tree
	"""block = ":" eoln indent stmtList undent"""

	match(":")
	match(";")
	match("@")
	statement = stmtList( )
	state = block( statement )
	tok = tokens.peek( )
	while tok != "~":
		next_statement = stmtList( )
		state.addStatement( next_statement )
		tok = tokens.peek( )
	match("~")
	return state

def parseWhileStatement( ): # parse rountine for while and uses the while class to print out the appropriate string
	"""whileStatement = "while"  expression  block"""

	tok = tokens.peek( )
	if debug: print( "whileStatement: ", tok )
	start = match( "while" )
	expr = expression( )
	blk = parseBlock( )
	tok = tokens.peek( )
	whileString = whileStatement( start, expr, blk )
	return whileString

def parseIfStatement( ): # parse rountine for the if and uses the if class to print out the appropriate string
	"""ifStatement = "if" expression block   [ "else" block ]"""

	tok = tokens.peek( )
	if debug: print( "ifStatement: ", tok )
	start = match( "if" )
	expr = expression( )
	blk = parseBlock( )
	elseblk = None
	tok = tokens.peek( )
	if tok == "else":
		match( "else" )
		elseblk = parseBlock( )
	return ifStatement(expr, blk, elseblk)

def parseAssign( ): # parse rountine for the assign and uses the assign class to print out the appropriate string 
	"""assign = ident "=" expression  eoln"""

	tok = tokens.peek( )
	if debug: print( "assign: ", tok )
	if re.match( Lexer.identifier, tok ):
		ident = VarRef( tok )
	else: 
		error( "Invalid identifier" )
	tok = tokens.next( )
	equals = match( "=" )
	tok = tokens.peek( )
	expr = expression( )
	match( ";" )
	equals = VarRef( equals )
	statement = assign( equals, ident, expr )
	return statement

def statement( ): # parse rountin for statement that makes sure the token is one of the following, eventually there will be an error caught 
	"""statement = ifStatement |  whileStatement  |  assign"""

	tok = tokens.peek( )
	if debug: print( "statement: ", tok )
	if tok == "if":
		stat = parseIfStatement( )
		return stat
	elif tok == "while":
		stat = parseWhileStatement( )
		return stat
	else: 
		stat = parseAssign( )
		return stat

def stmtList(  ):
	"""stmtList =  {  statement  }"""

	tok = tokens.peek( )
	if debug: print( "stmtList: ", tok )
	stat = statement( )
	return stat

def parseStmtList( tokens ):
	""" gee = { Statement } """

	tok = tokens.peek( )
	ast = list( ) # list that keeps track of the all the returns from the parse rountines 
	while tok is not None:
                # need to store each statement in a list
		statement = stmtList(  )
		ast.append( statement )
		tok = tokens.peek( )		
	return ast

def parse( text ) :
	global tokens
	tokens = Lexer( text )
	#expr = expression( )
	#print (str(expr))
	#     Or:
	#print(tokens)
	stmtlist = parseStmtList( tokens )
	statement = StmtList( stmtlist ) # uses the class to get a string that has all the proper "\n" for the variable to just print it out 
	print( statement )
	return


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

def mklines(filename):
	inn = open(filename, "r")
	lines = [ ]
	pos = [0]
	ct = 0
	for line in inn:
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
		print (ct, "\t", line)
		lines.append(line)
	# print len(pos)
	undent = ""
	for i in pos[1:]:
		undent += "~"
	lines.append(undent)
	# print undent
	return lines



def main():
	"""main program for testing"""
	
	global debug
	ct = 0
	for opt in sys.argv[1:]:
		if opt[0] != "-": break
		ct = ct + 1
		if opt == "-d": debug = True
	if len(sys.argv) < 2+ct:
		print ("Usage:  %s filename" % sys.argv[0])
		return
	parse("".join(mklines(sys.argv[1+ct])))
	return


main()