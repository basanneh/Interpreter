import os


class BinaryTree:

    def __init__(self, key):
        """Create new tree"""
        self._key = key
        self._child_left = None
        self._child_right = None

    def get_root_val(self):
        """Get root key value"""
        return self._key

    def set_root_val(self, key):
        """Set root key value"""
        self._key = key

    root = property(get_root_val, set_root_val)

    def get_child_left(self):
        """Get left child"""
        return self._child_left

    def set_child_left(self, node):
        """Set left child"""
        self._child_left = node

    child_left = property(get_child_left, set_child_left)

    def get_child_right(self):
        """Get right child"""
        return self._child_right

    def set_child_right(self, node):
        """Set right child"""
        self._child_right = node

    child_right = property(get_child_right, set_child_right)

    def is_leaf(self):
        """Check if a node is leaf"""
        return (not self._child_left) and (not self._child_right)

    def insert_left(self, new_node):
        """Insert left subtree"""
        if isinstance(new_node, BinaryTree):
            new_subtree = new_node
        else:
            new_subtree = BinaryTree(new_node)

        if self._child_left:
            new_subtree.set_child_left(self._child_left)

        self._child_left = new_subtree

    def insert_right(self, new_node):
        """Insert right subtree"""
        if isinstance(new_node, BinaryTree):
            new_subtree = new_node
        else:
            new_subtree = BinaryTree(new_node)

        if self._child_right:
            new_subtree.set_child_right(self._child_right)
        self._child_right = new_subtree

    def postorder(self):
        """Post-order tree traversal"""
        if self._child_left:
            self._child_left.postorder()
        if self._child_right:
            self._child_right.postorder()
        print(self._key, end=" ")


class Project:
    pass


# Global declarations 
# Variables 
charClass = 0
lexeme = []
nextChar = ''
token = 0
nextToken = 0
sourceLine = 1
f = open("Test.ada")
infix = []

keywords = {
    # Character classes
    'LETTER': 0,
    'DIGIT': 1,
    'UNKNOWN': 99,
    # Token codes
    'EOF': -1,
    'INT_LIT': 10,
    'FLOAT': 11,
    'IDENT': 12,
    'TERM': 13,
    'SEPER': 14,
    'FOW': 15,
    'OR': 16,
    'AND': 17,
    'DOT': 18,
    'ASSIGN_OP': 20,
    'ADD_OP': 21,
    'SUB_OP': 22,
    'MULT_OP': 23,
    'DIV_OP': 24,
    'LEFT_PAREN': 25,
    'RIGHT_PAREN': 26,
    'PROC': 30,
    'BEGIN': 31,
    'END': 32,
    'IS': 33,
    'DEC': 34,
    'WITH': 35,
    'USE': 36,
    'IF': 37,
    'THEN': 38,
    'ELIF': 39,
    'ELSE': 40,
    'CASE': 41,
    'OTHER': 42,
    'WHILE': 43,
    'FOR': 44,
    'LOOP': 45,
    'OF': 46,
    'INT_DEC': 50,
    'PUT_L': 60
}


##############################################################################################
#                                                                                            #
#                                       Scanner                                              #
#                                                                                            #
##############################################################################################


def keywordLookup():
    global lexeme, nextToken

    # Turn char list into string for comparison
    tempString = ""
    for i in lexeme:
        tempString += i

    # Test if a keyword is being inputted
    if tempString == 'procedure':
        nextToken = keywords['PROC']
        return True
    elif tempString == 'begin':
        nextToken = keywords['BEGIN']
        return True
    elif tempString == 'end':
        nextToken = keywords['END']
        return True
    elif tempString == 'is':
        nextToken = keywords['IS']
        return True
    elif tempString == 'declare':
        nextToken = keywords['DEC']
        return True
    elif tempString == 'Integer':
        nextToken = keywords['INT_DEC']
        return True
    elif tempString == 'Put_Line':
        nextToken = keywords['PUT_L']
        return True
    elif tempString == 'with':
        nextToken = keywords['WITH']
        return True
    elif tempString == 'use':
        nextToken = keywords['USE']
        return True
    elif tempString == 'if':
        nextToken = keywords['IF']
        return True
    elif tempString == 'then':
        nextToken = keywords['THEN']
        return True
    elif tempString == 'elif':
        nextToken = keywords['ELIF']
        return True
    elif tempString == 'else':
        nextToken = keywords['ELSE']
        return True
    elif tempString == 'case':
        nextToken = keywords['CASE']
        return True
    elif tempString == 'others':
        nextToken = keywords['OTHER']
        return True
    elif tempString == 'while':
        nextToken = keywords['WHILE']
        return True
    elif tempString == 'for':
        nextToken = keywords['FOR']
        return True
    elif tempString == 'loop':
        nextToken = keywords['LOOP']
        return True
    elif tempString == 'of':
        nextToken = keywords['OF']
        return True
    
    # The lexeme was not a keyword
    return False


def is_eof():
    # Get current position in file
    cur = f.tell()
    f.seek(0, os.SEEK_END)

    # Get size of file
    end = f.tell()
    f.seek(cur, os.SEEK_SET)

    # See if we are at the end of the file
    return cur == end


def addChar():
    global lexeme, nextChar

    # Append the next char to the lexeme list
    lexeme.append(nextChar)


def getChar():
    global charClass, nextChar

    # Read next char from file
    nextChar = f.read(1)

    # Test whether the char is a letter, digit, or something else
    if nextChar.isalpha() or nextChar == '_':
        charClass = keywords['LETTER']
    elif nextChar.isdigit():
        charClass = keywords['DIGIT']
    elif nextChar == '.':
        charClass = keywords['DOT']
    elif nextChar == '-':
        charClass = keywords['SUB_OP']
    else:
        charClass = keywords['UNKNOWN']


def getNonBlank():
    global nextChar

    # Remove white space so we can get to next lexeme
    while nextChar.isspace():  # == ' ':
        getChar()


def lex():
    global lexeme, nextToken, nextChar, sourceLine

    getNonBlank()

    # Detect if this is the end of the line, increment the source line, and output result to user
    if nextChar == '\n':
        print("End of source line " + str(sourceLine) + "\n")
        sourceLine += 1
        print("Start of source line " + str(sourceLine))
        getChar()
        return

    # See if the next char is classified as letter, digit, eof, or something else
    if charClass == keywords['LETTER']:
        addChar()
        getChar()
        while charClass == keywords['LETTER'] or charClass == keywords['DIGIT']:
            addChar()
            getChar()
        if not keywordLookup():
            nextToken = keywords['IDENT']
    elif charClass == keywords['SUB_OP']:
        addChar()
        getChar()
        if charClass == keywords['DIGIT']:
            while charClass == keywords['DIGIT'] or charClass == keywords['DOT']:
                addChar()
                getChar()
                if charClass == keywords['DOT']:
                    nextToken = keywords['FLOAT']
        else:
            nextToken = keywords['SUB_OP']
    elif charClass == keywords['DIGIT']:
        addChar()
        getChar()
        nextToken = keywords['INT_LIT']
        while charClass == keywords['DIGIT'] or charClass == keywords['DOT']:
            addChar()
            getChar()
            if charClass == keywords['DOT']:
                nextToken = keywords['FLOAT']
    elif is_eof():
        nextToken = keywords['EOF']
        lexeme.append('E')
        lexeme.append('O')
        lexeme.append('F')
    elif charClass == keywords['UNKNOWN']:
        lookup(nextChar)
        getChar()

    # Turn lexeme list into string for output to user, then clear list
    tempString = ""
    for i in lexeme:
        tempString += i
    if tempString != 'EOF':
        infix.append(tempString)
    print("Next token is: " + str(nextToken) + ", Next lexeme is " + tempString)

    lexeme = []
    print(expr())


def lookup(ch):
    global nextToken

    # Test all symbols that do something, else the unknown is just an identifier
    if ch == '(':
        addChar()
        nextToken = keywords['LEFT_PAREN']
    elif ch == ')':
        addChar()
        nextToken = keywords['RIGHT_PAREN']
    elif ch == '+':
        addChar()
        nextToken = keywords['ADD_OP']
    elif ch == '*':
        addChar()
        nextToken = keywords['MULT_OP']
    elif ch == '/':
        addChar()
        nextToken = keywords['DIV_OP']
    elif ch == ';':
        addChar()
        nextToken = keywords['TERM']
    elif ch == ':':
        addChar()
        getChar()
        if nextChar == '=':
            addChar()
            nextToken = keywords['ASSIGN_OP']
        else:
            nextToken = keywords['SEPER']
    elif ch == '=':
        addChar()
        getChar()
        if nextChar == '>':
            addChar()
            nextToken = keywords['FOW']
        else:
            nextToken = keywords['IDENT']
    elif ch == '|':
        addChar()
        nextToken = keywords['OR']
    elif ch == '&':
        addChar()
        nextToken = keywords['AND']
    else:
        addChar()
        nextToken = keywords['IDENT']
    
    return nextToken


##############################################################################################
#                                                                                            #
#                                       PARSER                                               #
#                                                                                            #
##############################################################################################


def error():
    print("Invalid Syntax")


def buildParseTree(fpexp):
    fplist = fpexp 
   
    pStack = []
    eTree = BinaryTree("")
   
    pStack.append(eTree)
    currentTree = eTree

    for i in fplist:
        if i == '(':
            currentTree.insert_left('')
            
            pStack.append(currentTree)
            currentTree = currentTree.get_child_left()

        elif i in ['+', '-', '*', '/','=']:
            currentTree.set_root_val(i)
            currentTree.insert_right('')
           
            pStack.append(currentTree)
            currentTree = currentTree.get_child_right()

        elif i == ')':
            
            currentTree = pStack.pop()

        elif i not in ['+', '-', '*', '/', ')']:
            try:
                currentTree.set_root_val(float(i))
                
                parent = pStack.pop()
                currentTree = parent

            except ValueError:
                raise ValueError("token '{}' is not a valid integer".format(i))

    return eTree

     
# Grammar
# <expr> -> <term> {(+ | -) <term>
# <term> -> <factor> {(* | /) <factor>
# <factor> -> id | int_constant | ( <expr )


# expr
# Parses strings in the language generated by the rule: <expr> -> <term> {(+ | -) <term>}
def expr():
    print("Enter <expr>\n")
    # Parse the first term 
    term()

# As long as the next token is + or -, get the next token and parse the next term 
    while nextToken == keywords['ADD_OP'] or nextToken == keywords['SUB_OP']:
        lex()
        term()
    print("Exit <expr>\n")

# term
# Parses strings in the language generated by the rule: <term> -> <factor> {(* | /) <factor>)


def term():
    print("Enter <term>\n")
    # Parse the first factor
    factor()
# As long as the next token is '*' or '/', get the next token and parse the next factor 
    while nextToken == keywords['MULT_OP'] or nextToken == keywords['DIV_OP']:
        lex()
        factor()
    print("Exit <term>\n")


# factor
# Parses strings in the language generated by the rule: <factor> -> id | int_constant | ( <expr )

def factor():
    print("Enter <factor>\n")


# Determine which RHS 
    if nextToken == keywords['IDENT'] or nextToken == keywords['INT_LIT']\
            or nextToken == keywords['DOT'] or nextToken == keywords['FLOAT']:
        # get the next token
        lex()

# If the RHS is ( <expr>), call lex to pass over the left parenthesis, call expr, and check for the right parenthesis
    else:
        if nextToken == keywords['LEFT_PAREN']:
            lex()
            expr()
            if nextToken == keywords['RIGHT_PAREN']:
                lex()
        #     else:
        #         error()
        # # Not an integer literal, or a left parenthesis

        # else:
        #     error()
    print("Exit <factor>\n")

##############################################################################################
#                                                                                            #
#                                       INTERPRETER                                          #
#                                                                                            #
##############################################################################################


# Traverse the tree and do a postfix ( Reverse Polish ) arithmetic calculation
def transCompileSwitch(parseTree):
    if parseTree is None:
        return -1
    operator ={'+', '-', '*', '/', ')'}
    if parseTree.get_child_left() is None and parseTree.get_child_right() is None:
        return float(parseTree.get_root_val())
    left_sum = transCompileSwitch(parseTree.get_child_left())
    right_sum = transCompileSwitch(parseTree.get_child_right())
    

    if parseTree.get_root_val() in operator:
        switcher = {
            '+': left_sum + right_sum,
            '-': left_sum - right_sum,
            '*': left_sum * right_sum,
            '/': left_sum / right_sum
        }
        return switcher.get(parseTree.get_root_val())


def main():
    # Open the input data file
    if f is None:
        print("ERROR - cannot open front.in \n")
    else:
        # Get first char
        getChar()

        print("Start of source line " + str(sourceLine))

        while True:
            # Continue scanning until the end of the file has been reached
            lex()
            if nextToken == keywords['EOF']:
                break
        
        print(infix)
        pt = buildParseTree(infix)
        print("Infix to Postfix : ")
        pt.postorder()
        print("\nRuntime Result: ", transCompileSwitch(pt))


##############################################################################################
#                                                                                            #
#                                            MAIN                                            #
#                                                                                            #
##############################################################################################


if __name__ == '__main__':
    main()