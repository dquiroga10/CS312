
import re, sys, string

debug = False
dict = { }
tokens = [ ]



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

class List(  ):
	def __init__(self):
		self.list = list( )

	def append( self, string ):
		self.list.append( string )

	def retList( self ):
		return self.list

class Statement( object ):
	def __str__(self):
		return ""


class block( Statement ):
	def __init__(self, statement):
		self.statement = str(statement)
		#self.second = None

	def addStatement(self, next_statement):
		self.statement = str(self.statement) + "\n" + str(next_statement)
		#return self.statement

	def __str__(self):
		return self.statement

class whileStatement( Statement ):
	def __init__(self, whilestr, expression, block):
		self.statement = str(str(whilestr) + " " + str(expression) + "\n" + str(block) + "\n" + "endwhile")

	def __str__(self):
		return self.statement

class ifStatement( Statement ):
	def __init__(self, ifstr, expression, block):
		self.statement = str(str(ifstr) + " " + str(expression) + "\n" + str(block) + "\n" + "else")

	def addElse(self, elseblk):
		self.statement = str(self.statement + "\n" + str(elseblk))

	def __str__(self):
		return self.statement + "\n" + "endif"

class assign( Statement ):
	def __init__(self, equals, identifier, expression):
		self.assign = str(str(equals) + " " + str(identifier) + " " + str(expression))
		
	def __str__(self):
		return self.assign

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
	left = andExpr( )
	#print(left)
	tok = tokens.peek( )
	while tok == "or":
		tokens.next()
		right = andExpr( )
		left = BinaryExpr(tok, left, right) # MIGHT HAVE TO CHANGE THIS TO STRING CAUSE ITS "or"
		tok = tokens.peek( )
	return left


def andExpr( ): #DOUBLE CHECK THIS 
	"""andExpr    = relationalExpr { "and" relationalExpr }"""

	tok = tokens.peek( )
	if debug: print("andExpr: ", tok)
	left = relationalExpr( )
	tok = tokens.peek( )
	while tok == "and":
		tokens.next()
		right = relationalExpr( )
		left = BinaryExpr(tok, left, right)#MIGHT HAVE TO CHANGE TO STRING 
		tok = tokens.peek( )
	return left 

relations    = ["==" , "!=" , "<" , "<=" , ">" , ">="]

def relationalExpr( ):#MAKE SURE I USED THE RIGHT LOGIC FOR THIS 
	"""relationalExpr = addExpr [ relation addExpr ]"""

	tok = tokens.peek( )
	if debug: print("relationalExpr: ", tok)
	left = addExpr( )
	expr = ""
	tok = tokens.peek( )
	#print(left)
	#print(tok)
	if tok in relations:
		#tok = tokens.next( )
		rel = relation( )
		right = expression( )
		expr = BinaryExpr( rel, left, right )
		#if tok in relation:
		#	expr = relation( )
		#elif tok != "]":
		#	expr = addExpr( )
		#match("]")
		return expr #fix this for syntax tree maybe

	return left
	# how to deal with regular brackets - if statement for each and then 
	#empty string? and if not either of them then error

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
	if re.match( Lexer.identifier, tok ):
		expr = VarRef(tok)
		tokens.next( )
		#print(tokens.peek( ))
		return expr

	error( "Invalid operand" )
	return


def term( ):
	""" term    = factor { ('*' | '/') factor } """

	tok = tokens.peek( )
	if debug: print ("Term: ", tok)
	left = factor( )
	tok = tokens.peek( )
	#print(left)
	while tok == "*" or tok == "/":
		tokens.next()
		right = factor( )
		#print(right)
		left = BinaryExpr( tok, left, right )
		tok = tokens.peek( )
	return left

def addExpr( ):
	""" addExpr    = term { ('+' | '-') term } """

	tok = tokens.peek( )
	if debug: print ("addExpr: ", tok)
	left = term( )
	tok = tokens.peek( )
	#print(left)
	while tok == "+" or tok == "-":
		#print(tok)
		tokens.next()
		#print(tokens.peek( ))
		right = term( )
		#print(tokens.peek( ))
		left = BinaryExpr( tok, left, right )
		#print(left)
		tok = tokens.peek( )
		#print(tok)
	return left

def parseBlock( ):
	"""block = ":" eoln indent stmtList undent"""
	match(":")
	match(";")
	match("@")
	statement = stmtList( )
	state = block( statement )
	tok = tokens.peek( )
	while tok != "~":
		next_statement = stmtList( )
		#stat = String(str(stat) + "\n" + str(second_stat))
		state.addStatement( next_statement )
		tok = tokens.peek( )
	match("~")
	#string = str(stat)
	return state

def parseWhileStatement( ): 
	"""whileStatement = "while"  expression  block"""
	tok = tokens.peek( )
	if debug: print( "whileStatement: ", tok )
	start = match( "while" )
	expr = expression( )
	blk = parseBlock( )
	tok = tokens.peek( )
	whileString = whileStatement( start, expr, blk )
	return whileString

def parseIfStatement( ):
	"""ifStatement = "if" expression block   [ "else" block ]"""
	tok = tokens.peek( )
	if debug: print( "ifStatement: ", tok )
	start = match( "if" )
	expr = expression( )
	blk = parseBlock( )
	elseblk = None
	ifState = ifStatement( start, expr, blk )
	#ifString = String(str(start) + " " + str(expr) + "\n" + str(blk) + "\n" + "else") #ifString = String(str(start) + " " + str(expr) + "\n" + str(blk)) 
	tok = tokens.peek( )
	#print(tok)
	if tok == "else":
		match( "else" )
		elseblk = parseBlock( )
		ifState.addElse( elseblk )
		#ifString = String(str(ifString) + "\n" + str(left))#ifString = String(str(ifString) + "\n" + str(right) + "\n" + str(left))
	#ifString = String(str(ifString) + "\n" + "endif")
	return ifState

def parseAssign( ):
	"""assign = ident "=" expression  eoln"""
	tok = tokens.peek( )
	if debug: print( "assign: ", tok )
	if re.match( Lexer.identifier, tok ):
		ident = VarRef( tok )
		#print(left)
	else: 
		error( "Invalid identifier" )
	tok = tokens.next( )
	#print(tok)
	equals = match( "=" )
	tok = tokens.peek( )
	#print( tok )
	expr = expression( )
	match( ";" )
	equals = VarRef( equals )
	statement = assign( equals, ident, expr )
	#stat = BinaryExpr(op, left, right)
	#print(stat)
	#print(tokens.peek( ))
	return statement

def statement( ):
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
	#while tok is not ";": #change this most likely
	#print(tokens)
	stat = statement( )
	#tokens.next()
	#tok = tokens.peek( )
	#print(tok)
	#	break
	return stat

def parseStmtList( tokens ):
	""" gee = { Statement } """
	tok = tokens.peek( )
	ast = List( )
	while tok is not None:
                # need to store each statement in a list
		#ast = parseStmt(tokens) this is the original changed it for the start symbol
		statement = stmtList(  )
		#print("statement: " + "\n" + str(statement))
		ast.append( statement )
		tok = tokens.peek( )
		#print("tok: " + str(tok))
		
	return ast #TODO: change this so that its an object of Expression
def parse( text ) :
	global tokens
	tokens = Lexer( text )
	#expr = expression( )
	#print (str(expr))
	#     Or:
	#print(tokens)
	stmtlist = parseStmtList( tokens )
	statements = stmtlist.retList( )
	#print(elsecount)
	#count = 1
	for i in statements:
		count = 0
		count = str(i).count("else" + "\n" + "=")
		count += str(i).count("else" + "\n" + "while ")
		count += str(i).count("else" + "\n" + "if ")
		print(count)
		#elsecount = str(i).count("else")
		#ifcount = str(i).count("if")
		#print(elsecount, ifcount)
		if count == 0:
			i = str(i).replace("\n" + "else", "")
		print( i )
		#count += 1
	#print(str(stmtlist))
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