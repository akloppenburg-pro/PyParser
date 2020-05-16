import re

# booleans used to set the type for the tokens we find
isKey = False
isID = False
isConst = False

# flags to tell us when the error handler has been called and for what type of error
invalid_const_two_decimals = False
invalid_ss = False
invalid_const_letter = False
const_starting_decimal = False
id_starting_decimal = False

# SYMTAB array (2x100) and counter variable to determine our place in the table
k = 100
j = 2
SYMTAB = [[None] * j for i in range(k)]
table_row = 0

# integer codes for use with PARSER()
STACK_BOTTOM = 0
T_ID = 1
T_CONST = 2
T_DEF = 3
T_MAIN = 4
T_READ = 5
T_PRINT = 6
T_IMPORT = 7
T_GLOBAL = 8
T_BREAK = 9
T_CONTINUE = 10
T_RETURN = 11
T_IF = 12
T_ELSEIF = 13
T_ELSE = 14
T_WHILE = 15
T_NOT = 16
T_TRUE = 17
T_FALSE = 18
T_AND = 19
T_OR = 20
T_COLON = 21
T_COMMA = 22
T_SEMICOLON = 23
T_L_PARENS = 24
T_R_PARENS = 25
T_L_BRACKET = 26
T_R_BRACKET = 27
T_EQ = 28
T_LT = 29
T_GT = 30
T_PLUS = 31
T_MULT = 32
T_AT = 33
NT_PYTHON = 34
NT_DEF = 35
NT_MORE_DEFS = 36
NT_PARA_LIST = 37
NT_BLOCK = 38
NT_ID_LIST = 39
NT_MORE_IDS = 40
NT_STMTS = 41
NT_MORE_STMTS = 42
NT_STMT = 43
NT_INPUT = 44
NT_OUTPUT = 45
NT_ASMT = 46
NT_EXPR_LIST = 47
NT_EXPR = 48
NT_MORE_EXPRS = 49
NT_IMPORT = 50
NT_GLOBAL = 51
NT_FLOW = 52
NT_COND = 53
NT_ELSEIF = 54
NT_ELSEIF_LIST = 55
NT_MORE_ELSEIF = 56
NT_ELSE = 57
NT_LOOP = 58
NT_BOOL_EXPR = 59
NT_BOOL = 69
NT_COMP = 61
NT_ARITH_EXPR = 62
NT_ARITH = 63

# PARSER() stack array, max size is 100
stack = []

input = ''


def MAIN():
    # read in input file
    in_file = open('parser_input.txt', 'r')

    # store in a variable so we can pass it to main
    global input
    input = in_file.read()

    # write input file to our big output file
    out_file = open('output.txt', 'w')
    out_file.write(input)
    out_file.write("\n\n\n")
    # close output file, since all writing after this should be appended to the end of the file
    out_file.close()

    # loop through until input is empty
    PARSER()

    # print our symtab table
    out_file = open('output.txt', 'a')
    out_file.write("\n\n")
    for row in SYMTAB:
        out_file.write(str(row) + "\n")
    # close the output file
    out_file.close()

def PARSER():
    # bring input into the function to be used by SCANNER()
    global input

    # open output file to be written to
    out_file = open('output.txt', 'a')

    # initialize step counter
    steps = 0
    # initialize lookahead
    lookahead = None
    # add stack bottom marker to the stack
    stack.append(STACK_BOTTOM)

    # increment step counter
    steps += 1
    # output step taken to file
    out_file.write(outputWriter(steps, stack[-1], lookahead, 'ss') + "\n")
    # add start symbol to stack
    stack.append(NT_PYTHON)

    # scanner loop
    while input != "":
        # get a lookahead token
        lookahead = SCANNER()
        # enter EXPAND loop
        while lookahead is None or (stack[-1] != lookahead[1]):
            # if the stack bottom marker is on top of the stack, we can accept
            if stack[-1] == STACK_BOTTOM:
                # increment step counter
                steps += 1
                # write out accept case and exit program
                out_file.write(outputWriter(steps, stack[-1], lookahead, "accept"))
                return
            # rule 1
            if stack[-1] == NT_PYTHON and lookahead[1] == T_DEF:
                print("entered rule 1")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "1\n")
                # expand using rule 1
                stack.pop()
                stack.append(NT_MORE_DEFS)
                stack.append(NT_DEF)
            # rule 2
            elif stack[-1] == NT_DEF and lookahead[1] == T_DEF:
                print("entered rule 2")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "2\n")
                # expand using rule 2
                stack.pop()
                stack.append(NT_BLOCK)
                stack.append(T_COLON)
                stack.append(T_R_PARENS)
                stack.append(NT_PARA_LIST)
                stack.append(T_L_PARENS)
                stack.append(T_ID)
                stack.append(T_DEF)
            # rule 3
            elif stack[-1] == NT_MORE_DEFS and lookahead is None:
                print("entered rule 3")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "3\n")
                # expand using rule 3
                stack.pop()     # this is how we do epsilon
            # rule 4
            elif stack[-1] == NT_MORE_DEFS and lookahead[1] == T_DEF:
                print("entered rule 4")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "4\n")
                # expand using rule 4
                stack.pop()
                stack.append(NT_MORE_DEFS)
                stack.append(NT_DEF)
            # rule 5
            elif stack[-1] == NT_PARA_LIST and lookahead[1] == T_R_PARENS:
                print("entered rule 5")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "5\n")
                # expand using rule 5
                stack.pop()     # this is how we do epsilon
            # rule 6
            elif stack[-1] == NT_PARA_LIST and lookahead[1] == T_ID:
                print("entered rule 6")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "6\n")
                # expand using rule 6
                stack.pop()
                stack.append(NT_ID_LIST)
            # rule 7
            elif stack[-1] == NT_BLOCK and (lookahead[1] == T_READ or lookahead[1] == T_PRINT or lookahead[1] == T_ID
                                            or lookahead[1] == T_IMPORT or lookahead[1] == T_GLOBAL or
                                            lookahead[1] == T_BREAK or lookahead[1] == T_CONTINUE or
                                            lookahead[1] == T_RETURN or lookahead[1] == T_IF or
                                            lookahead[1] == T_WHILE):
                print("entered rule 7")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "7\n")
                # expand using rule 7
                stack.pop()
                stack.append(NT_STMT)
            # rule 8
            elif stack[-1] == NT_BLOCK and lookahead[1] == T_L_BRACKET:
                print("entered rule 8")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "8\n")
                # expand using rule 8
                stack.pop()
                stack.append(T_R_BRACKET)
                stack.append(NT_STMTS)
                stack.append(T_L_BRACKET)
            # rule 9
            elif stack[-1] == NT_ID_LIST and lookahead[1] == T_ID:
                print("entered rule 9")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "9\n")
                # expand using rule 9
                stack.pop()
                stack.append(NT_MORE_IDS)
                stack.append(T_ID)
            # rule 10
            elif stack[-1] == NT_MORE_IDS and (lookahead[1] == T_R_PARENS or lookahead[1] == T_EQ or
                                               lookahead[1] == T_DEF or lookahead[1] == T_ELSEIF or
                                               lookahead[1] == T_ELSE or lookahead[1] == T_SEMICOLON or
                                               lookahead[1] == T_R_BRACKET):
                print("entered rule 10")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "10\n")
                # expand using rule 10
                stack.pop()  # this is how we do epsilon
            # rule 11
            elif stack[-1] == NT_MORE_IDS and lookahead[1] == T_COMMA:
                print("entered rule 11")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "11\n")
                # expand using rule 11
                stack.pop()
                stack.append(NT_MORE_IDS)
                stack.append(T_ID)
                stack.append(T_COMMA)
            # rule 12
            elif stack[-1] == NT_STMTS and (lookahead[1] == T_READ or lookahead[1] == T_PRINT or lookahead[1] == T_ID
                                            or lookahead[1] == T_IMPORT or lookahead[1] == T_GLOBAL or
                                            lookahead[1] == T_BREAK or lookahead[1] == T_CONTINUE or
                                            lookahead[1] == T_RETURN or lookahead[1] == T_IF or
                                            lookahead[1] == T_WHILE):
                print("entered rule 12")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "12\n")
                # expand using rule 12
                stack.pop()
                stack.append(NT_MORE_STMTS)
                stack.append(NT_STMT)
            # rule 13
            elif stack[-1] == NT_MORE_STMTS and lookahead[1] == T_R_BRACKET:
                print("entered rule 13")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "13\n")
                # expand using rule 13
                stack.pop()     # epsilon
            # rule 14
            elif stack[-1] == NT_MORE_STMTS and lookahead[1] == T_SEMICOLON:
                print("entered rule 14")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "14\n")
                # expand using rule 14
                stack.pop()
                stack.append(NT_MORE_STMTS)
                stack.append(NT_STMT)
                stack.append(T_SEMICOLON)
            # rule 15
            elif stack[-1] == NT_STMT and lookahead[1] == T_READ:
                print("entered rule 15")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "15\n")
                # expand using rule 15
                stack.pop()
                stack.append(NT_INPUT)
            # rule 16
            elif stack[-1] == NT_STMT and lookahead[1] == T_PRINT:
                print("entered rule 15")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "16\n")
                # expand using rule 16
                stack.pop()
                stack.append(NT_OUTPUT)
            # rule 17
            elif stack[-1] == NT_STMT and lookahead[1] == T_ID:
                print("entered rule 17")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "17\n")
                # expand using rule 17
                stack.pop()
                stack.append(NT_ASMT)
            # rule 18
            elif stack[-1] == NT_STMT and lookahead[1] == T_IMPORT:
                print("entered rule 18")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "18\n")
                # expand using rule 18
                stack.pop()
                stack.append(NT_IMPORT)
            # rule 19
            elif stack[-1] == NT_STMT and lookahead[1] == T_GLOBAL:
                print("entered rule 19")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "19\n")
                # expand using rule 19
                stack.pop()
                stack.append(NT_GLOBAL)
            # rule 20
            elif stack[-1] == NT_STMT and (lookahead[1] == T_BREAK or lookahead[1] == T_CONTINUE or
                                           lookahead[1] == T_RETURN):
                print("entered rule 20")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "20\n")
                # expand using rule 20
                stack.pop()
                stack.append(NT_FLOW)
            # rule 21
            elif stack[-1] == NT_STMT and lookahead[1] == T_IF:
                print("entered rule 21")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "21\n")
                # expand using rule 21
                stack.pop()
                stack.append(NT_COND)
            # rule 22
            elif stack[-1] == NT_STMT and lookahead[1] == T_WHILE:
                print("entered rule 22")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "22\n")
                # expand using rule 22
                stack.pop()
                stack.append(NT_LOOP)
            # rule 23
            elif stack[-1] == NT_INPUT and lookahead[1] == T_READ:
                print("entered rule 23")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "23\n")
                # expand using rule 23
                stack.pop()
                stack.append(T_R_PARENS)
                stack.append(NT_ID_LIST)
                stack.append(T_L_PARENS)
                stack.append(T_READ)
            # rule 24
            elif stack[-1] == NT_OUTPUT and lookahead[1] == T_PRINT:
                print("entered rule 24")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "24\n")
                # expand using rule 23
                stack.pop()
                stack.append(T_R_PARENS)
                stack.append(NT_ID_LIST)
                stack.append(T_L_PARENS)
                stack.append(T_PRINT)
            # rule 25
            elif stack[-1] == NT_ASMT and lookahead[1] == T_ID:
                print("entered rule 25")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "25\n")
                # expand using rule 25
                stack.pop()
                stack.append(NT_EXPR_LIST)
                stack.append(T_EQ)
                stack.append(NT_ID_LIST)
            # rule 26
            elif stack[-1] == NT_EXPR_LIST and (lookahead[1] == T_NOT or lookahead[1] == T_TRUE or
                                                lookahead[1] == T_FALSE or lookahead[1] == T_LT or lookahead[1] == T_EQ
                                                or lookahead[1] == T_GT or lookahead[1] == T_ID or
                                                lookahead[1] == T_CONST or lookahead[1] == T_L_PARENS or
                                                lookahead[1] == T_AT):
                print("entered rule 26")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "26\n")
                # expand using rule 26
                stack.pop()
                stack.append(NT_MORE_EXPRS)
                stack.append(NT_EXPR)
            # rule 27
            elif stack[-1] == NT_EXPR and (lookahead[1] == T_NOT or lookahead[1] == T_TRUE or
                                                lookahead[1] == T_FALSE or lookahead[1] == T_LT or
                                                lookahead[1] == T_EQ or lookahead[1] == T_GT):
                print("entered rule 27")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "27\n")
                # expand using rule 27
                stack.pop()
                stack.append(NT_BOOL_EXPR)
            # rule 28
            elif stack[-1] == NT_EXPR and (lookahead[1] == T_ID or lookahead[1] == T_CONST or
                                                lookahead[1] == T_L_PARENS):
                print("entered rule 28")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "28\n")
                # expand using rule 28
                stack.pop()
                stack.append(NT_ARITH_EXPR)
            # rule 29
            elif stack[-1] == NT_EXPR and lookahead[1] == T_AT:
                print("entered rule 29")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "29\n")
                # expand using rule 28
                stack.pop()
                stack.append(T_R_PARENS)
                stack.append(NT_PARA_LIST)
                stack.append(T_L_PARENS)
                stack.append(T_ID)
                stack.append(T_AT)
            # rule 30
            elif stack[-1] == NT_MORE_EXPRS and (lookahead[1] == T_DEF or lookahead[1] == T_ELSEIF or
                                                 lookahead[1] == T_ELSE or lookahead[1] == T_SEMICOLON or
                                                 lookahead[1] == T_R_BRACKET):
                print("entered rule 30")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "30\n")
                # expand using rule 13
                stack.pop()  # epsilon
            # rule 31
            elif stack[-1] == NT_MORE_EXPRS and lookahead[1] == T_COMMA:
                print("entered rule 31")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "31\n")
                # expand using rule 31
                stack.pop()
                stack.append(NT_MORE_EXPRS)
                stack.append(NT_EXPR)
                stack.append(T_COMMA)
            # rule 32
            elif stack[-1] == NT_IMPORT and lookahead[1] == T_IMPORT:
                print("entered rule 32")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "32\n")
                # expand using rule 32
                stack.pop()
                stack.append(T_ID)
                stack.append(T_IMPORT)
            # rule 33
            elif stack[-1] == NT_GLOBAL and lookahead[1] == T_GLOBAL:
                print("entered rule 33")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "33\n")
                # expand using rule 33
                stack.pop()
                stack.append(NT_ID_LIST)
                stack.append(T_GLOBAL)
            # rule 34
            elif stack[-1] == NT_FLOW and lookahead[1] == T_BREAK:
                print("entered rule 34")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "34\n")
                # expand using rule 34
                stack.pop()
                stack.append(T_BREAK)
            # rule 35
            elif stack[-1] == NT_FLOW and lookahead[1] == T_CONTINUE:
                print("entered rule 35")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "35\n")
                # expand using rule 35
                stack.pop()
                stack.append(T_CONTINUE)
            # rule 36
            elif stack[-1] == NT_FLOW and lookahead[1] == T_RETURN:
                print("entered rule 36")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "36\n")
                # expand using rule 36
                stack.pop()
                stack.append(NT_EXPR)
                stack.append(T_RETURN)
            # rule 37
            elif stack[-1] == NT_COND and lookahead[1] == T_IF:
                print("entered rule 37")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "37\n")
                # expand using rule 11
                stack.pop()
                stack.append(NT_ELSE)
                stack.append(NT_ELSEIF)
                stack.append(NT_BLOCK)
                stack.append(T_COLON)
                stack.append(NT_BOOL_EXPR)
                stack.append(T_IF)
            # rule 38
            elif stack[-1] == NT_ELSEIF and lookahead[1] == T_ELSE:
                print("entered rule 38")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "38\n")
                # expand using rule 38
                stack.pop()     #epsilon
            # rule 39
            elif stack[-1] == NT_ELSEIF and lookahead[1] == T_ELSEIF:
                print("entered rule 39")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "39\n")
                # expand using rule 39
                stack.pop()
                stack.append(NT_ELSEIF_LIST)
            # rule 40
            elif stack[-1] == NT_ELSEIF_LIST and lookahead[1] == T_ELSEIF:
                print("entered rule 40")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "40\n")
                # expand using rule 40
                stack.pop()
                stack.append(NT_MORE_ELSEIF)
                stack.append(NT_BLOCK)
                stack.append(T_COLON)
                stack.append(NT_BOOL_EXPR)
                stack.append(T_ELSEIF)
            # rule 41
            elif stack[-1] == NT_MORE_ELSEIF and lookahead[1] == T_ELSE:
                print("entered rule 41")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "41\n")
                # expand using rule 41
                stack.pop()     #epsilon
            # rule 42
            elif stack[-1] == NT_MORE_ELSEIF and lookahead[1] == T_ELSEIF:
                print("entered rule 42")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "42\n")
                # expand using rule 42
                stack.pop()
                stack.append(NT_ELSEIF_LIST)
            # rule 43
            elif stack[-1] == NT_ELSE and lookahead[1] == T_ELSE:
                print("entered rule 43")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "43\n")
                # expand using rule 43
                stack.pop()
                stack.append(NT_BLOCK)
                stack.append(T_COLON)
                stack.append(T_ELSE)
            # rule 44
            elif stack[-1] == NT_LOOP and lookahead[1] == T_WHILE:
                print("entered rule 44")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "44\n")
                # expand using rule 44
                stack.pop()
                stack.append(NT_BLOCK)
                stack.append(T_COLON)
                stack.append(NT_BOOL_EXPR)
                stack.append(T_WHILE)
            # rule 45
            elif stack[-1] == NT_BOOL_EXPR and lookahead[1] == T_NOT:
                print("entered rule 45")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "45\n")
                # expand using rule 11
                stack.pop()
                stack.append(NT_BOOL)
                stack.append(T_R_PARENS)
                stack.append(NT_BOOL_EXPR)
                stack.append(T_L_PARENS)
                stack.append(T_NOT)
            # rule 46
            elif stack[-1] == NT_BOOL_EXPR and lookahead[1] == T_TRUE:
                print("entered rule 46")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "46\n")
                # expand using rule 11
                stack.pop()
                stack.append(NT_BOOL)
                stack.append(T_TRUE)
            # rule 47
            elif stack[-1] == NT_BOOL_EXPR and lookahead[1] == T_FALSE:
                print("entered rule 47")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "47\n")
                # expand using rule 47
                stack.pop()
                stack.append(NT_BOOL)
                stack.append(T_FALSE)
            # rule 48
            elif stack[-1] == NT_BOOL_EXPR and (lookahead[1] == T_LT or lookahead[1] == T_EQ or lookahead[1] == T_GT):
                print("entered rule 48")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "48\n")
                # expand using rule 48
                stack.pop()
                stack.append(NT_ARITH_EXPR)
                stack.append(NT_ARITH_EXPR)
                stack.append(NT_COMP)
            # rule 49
            elif stack[-1] == NT_BOOL and (lookahead[1] == T_COMMA or lookahead[1] == T_COLON or
                                           lookahead[1] == T_R_PARENS or lookahead[1] == T_DEF or
                                           lookahead[1] == T_ELSEIF or lookahead[1] == T_ELSE or
                                           lookahead[1] == T_SEMICOLON or lookahead[1] == T_R_BRACKET):
                print("entered rule 49")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "49\n")
                # expand using rule 49
                stack.pop()     #epsilon
            # rule 50
            elif stack[-1] == NT_BOOL and lookahead[1] == T_AND:
                print("entered rule 50")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "50\n")
                # expand using rule 50
                stack.pop()
                stack.append(NT_BOOL_EXPR)
                stack.append(T_AND)
            # rule 51
            elif stack[-1] == NT_BOOL and lookahead[1] == T_OR:
                print("entered rule 51")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "51\n")
                # expand using rule 51
                stack.pop()
                stack.append(NT_BOOL_EXPR)
                stack.append(T_OR)
            # rule 52
            elif stack[-1] == NT_COMP and lookahead[1] == T_LT:
                print("entered rule 52")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "52\n")
                # expand using rule 52
                stack.pop()
                stack.append(T_LT)
            # rule 53
            elif stack[-1] == NT_COMP and lookahead[1] == T_EQ:
                print("entered rule 53")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "53\n")
                # expand using rule 53
                stack.pop()
                stack.append(T_EQ)
            # rule 54
            elif stack[-1] == NT_COMP and lookahead[1] == T_GT:
                print("entered rule 54")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "54\n")
                # expand using rule 54
                stack.pop()
                stack.append(T_GT)
            # rule 55
            elif stack[-1] == NT_ARITH_EXPR and lookahead[1] == T_ID:
                print("entered rule 55")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "55\n")
                # expand using rule 55
                stack.pop()
                stack.append(NT_ARITH)
                stack.append(T_ID)
            # rule 56
            elif stack[-1] == NT_ARITH_EXPR and lookahead[1] == T_CONST:
                print("entered rule 56")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "56\n")
                # expand using rule 56
                stack.pop()
                stack.append(NT_ARITH)
                stack.append(T_CONST)
            # rule 57
            elif stack[-1] == NT_ARITH_EXPR and lookahead[1] == T_L_PARENS:
                print("entered rule 57")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "57\n")
                # expand using rule 57
                stack.pop()
                stack.append(NT_ARITH)
                stack.append(T_R_PARENS)
                stack.append(NT_ARITH_EXPR)
                stack.append(T_L_PARENS)
            # rule 58
            elif stack[-1] == NT_ARITH and (lookahead[1] == T_COMMA or lookahead[1] == T_COLON or
                                            lookahead[1] == T_R_PARENS or lookahead[1] == T_ID or
                                            lookahead[1] == T_CONST or lookahead[1] == T_L_PARENS or
                                            lookahead[1] == T_DEF or lookahead[1] == T_ELSEIF or
                                            lookahead[1] == T_ELSE or lookahead[1] == T_SEMICOLON or
                                            lookahead[1] == T_R_BRACKET):
                print("entered rule 58")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "58\n")
                # expand using rule 58
                stack.pop()     #epsilon
            # rule 59
            elif stack[-1] == NT_ARITH and lookahead[1] == T_PLUS:
                print("entered rule 59")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "59\n")
                # expand using rule 59
                stack.pop()
                stack.append(NT_ARITH_EXPR)
                stack.append(T_PLUS)
            # rule 60
            elif stack[-1] == NT_ARITH and lookahead[1] == T_MULT:
                print("entered rule 60")
                # increment step counter
                steps += 1
                # output step taken to file
                out_file.write(outputWriter(steps, stack[-1], lookahead, "expand") + "60\n")
                # expand using rule 11
                stack.pop()
                stack.append(NT_ARITH_EXPR)
                stack.append(T_MULT)
            else:
                print("failed - stack: " + toName(stack[-1]) + " & lookahead: " + str(lookahead))
                return

        # once the loop is exited, we know that the stack top is equal to the token, and we can consume it
        # increment step counter
        steps += 1
        # output step taken to file
        print("popped " + toName(stack[-1]))
        out_file.write(outputWriter(steps, stack[-1], lookahead, "consume") + "\n")
        # consume token
        stack.pop()
    # close output file
    out_file.close()


def SCANNER():
    # pull our global variables into the function
    global isKey
    global isID
    global isConst
    global invalid_const_two_decimals
    global invalid_ss
    global invalid_const_letter
    global const_starting_decimal
    global id_starting_decimal

    global input

    # reset our token variable to empty
    token = ''
    # reset our token type flags to false
    isKey = False
    isID = False
    isConst = False
    # reset our error flags to false
    invalid_const_two_decimals = False
    invalid_ss = False
    invalid_const_letter = False
    const_starting_decimal = False
    id_starting_decimal = False

    # main loop within SCANNER, goes line by line and breaks if a token is recognized
    # going line by line allows us to exclude whole line if a comment is detected
    for line in input.splitlines(keepends=True):
        # counter to help us keep track of what character we're on
        currchar = 0
        # everything within this for loop is our DFA implementation -
        for char in line:
            # block to recognize comments
            # -----------------------------------------------------------------------------------------------
            if char == '#':
                # remove whatever is left of the line (aka the comment) from our input string
                # comment_length = len(line) - currchar
                input = input[len(line):]
                print("comment ignored")
                break

            # block to recognize special symbols, whitespace, or line breaks
            # -----------------------------------------------------------------------------------------------
            # encountering any of these mean the token is complete
            elif (char == ':' or char == ',' or char == ';' or char == '(' or char == ')' or char == '[' or char == ']'
                  or char == '=' or char == '<' or char == '>' or char == '+' or char == '*' or char == '@'
                  or char == ' ' or char == '\n' or char == ''):
                # if there hasn't been an error (aka the symbol is valid), the token is not a keyword, and the token
                # is not the empty string, check to see if it is in the symbol table.  If not, put it in
                if (not invalid_const_letter and not invalid_const_two_decimals and not invalid_ss and not
                const_starting_decimal and not id_starting_decimal):

                    # a boolean variable used to check if the given token already exists in the symbol table
                    is_in_table = False

                    # if the token is a keyword, return the appropriate pair based on what keyword it is
                    if isKey:
                        # shorten our input
                        input = input[len(token):]

                        if token == 'def':
                            return token, T_DEF
                        elif token == 'main':
                            return token, T_MAIN
                        elif token == 'read':
                            return token, T_READ
                        elif token == 'print':
                            return token, T_PRINT
                        elif token == 'import':
                            return token, T_IMPORT
                        elif token == 'global':
                            return token, T_GLOBAL
                        elif token == 'break':
                            return token, T_BREAK
                        elif token == 'continue':
                            return token, T_CONTINUE
                        elif token == 'return':
                            return token, T_RETURN
                        elif token == 'if':
                            return token, T_IF
                        elif token == 'elseif':
                            return token, T_ELSEIF
                        elif token == 'else':
                            return token, T_ELSE
                        elif token == 'while':
                            return token, T_WHILE
                        elif token == 'not':
                            return token, T_NOT
                        elif token == 'true':
                            return token, T_TRUE
                        elif token == 'false':
                            return token, T_FALSE
                        elif token == 'and':
                            return token, T_AND
                        elif token == 'or':
                            return token, T_OR
                    elif isConst:
                        # check symtab to see if we've already put it in there
                        for row in range(100):
                            if SYMTAB[row][0] == token:
                                is_in_table = True
                        # if the symbol is not in the symtab, put it in there
                        if not is_in_table:
                            BOOKKEEPER(token)
                        # shorten our input
                        input = input[len(token):]
                        # return the symbol to be used in PARSER()
                        return token, T_CONST
                    elif isID:
                        # check symtab to see if we've already put it in there
                        for row in range(100):
                            if SYMTAB[row][0] == token:
                                is_in_table = True
                        # if the symbol is not in the symtab, put it in there
                        if not is_in_table:
                            BOOKKEEPER(token)
                        # shorten our input
                        input = input[len(token):]
                        # return the symbol to be used in PARSER()
                        return token, T_ID
                    # if none of the flags have been tripped then we most likely have a special symbol
                    elif char != ' ' and char != "\n" and char != '':
                        # shorten our input by 1 to account for the char
                        input = input[1:]
                        if char == ':':
                            return char, T_COLON
                        elif char == ',':
                            return char, T_COMMA
                        elif char == ';':
                            return char, T_SEMICOLON
                        elif char == '(':
                            return char, T_L_PARENS
                        elif char == ')':
                            return char, T_R_PARENS
                        elif char == '[':
                            return char, T_L_BRACKET
                        elif char == ']':
                            return char, T_R_BRACKET
                        elif char == '=':
                            return char, T_EQ
                        elif char == '<':
                            return char, T_LT
                        elif char == '>':
                            return char, T_GT
                        elif char == '+':
                            return char, T_PLUS
                        elif char == '*':
                            return char, T_MULT
                        elif char == '@':
                            return char, T_AT
                    else:
                        input = input[1:]
                # if there is an error, call the error handler on it
                else:
                    ERRORHANDLER(token)
                    # shorten our input to account for the error token
                    input = input[len(token):]
                    # then, if our delimiter is a special symbol, write it to the output file as well
                    if char != ' ' and char != "\n" and char != '':
                        # shorten our input by 1 to account for the char
                        input = input[1:]
                        if char == ':':
                            return char, T_COLON
                        elif char == ',':
                            return char, T_COMMA
                        elif char == ';':
                            return char, T_SEMICOLON
                        elif char == '(':
                            return char, T_L_PARENS
                        elif char == ')':
                            return char, T_R_PARENS
                        elif char == '[':
                            return char, T_L_BRACKET
                        elif char == ']':
                            return char, T_R_BRACKET
                        elif char == '=':
                            return char, T_EQ
                        elif char == '<':
                            return char, T_LT
                        elif char == '>':
                            return char, T_GT
                        elif char == '+':
                            return char, T_PLUS
                        elif char == '*':
                            return char, T_MULT
                        elif char == '@':
                            return char, T_AT
                    else:
                        input = input[1:]

            # this block accepts a . with an empty token.  this is an error, but we find out if it's a constant error
            # or identifier error later on
            elif token == '' and char == '.':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize constants
            # --------------------------------------------------------------------------------------------
            # recognizes the start of a new constant (empty token string and our character is a number)
            # we accept . here (even though it's an error) so we can figure out if it's a constant or ID error
            elif token == '' and char.isdigit():
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isConst flag to True because we now have a constant variable
                isConst = True
            # recognizes the error case where a constant starts with a period
            elif token == '.' and char.isdigit():
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the appropriate error flag
                const_starting_decimal = True
            # recognizes if our token has ONLY numbers and our character is a number
            elif token.isdigit() and char.isdigit():
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            # recognizes if our token has ONLY numbers and our character is a decimal point
            elif token.isdigit() and char == '.':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            # recognizes if our token contains ONE decimal point and our character is a number
            elif isFloat(token) and char.isdigit():
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            # recognizes the error case where our token contains numbers (and maybe .) and our char is a letter
            elif isFloat(token) and char.isalpha():
                # set the appropriate error flag
                invalid_const_letter = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            # recognizes the error case where our token contains a . and our character is a second .
            elif isFloat(token) and char == '.':
                # set the appropriate error flag
                invalid_const_two_decimals = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            # recognizes the error case where our token starts with a . and our char is a number
            elif token != '' and token[0] == '.' and char.isdigit():
                # set the appropriate error flag
                const_starting_decimal = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize keywords, and identifiers if no keyword is registered
            # -------------------------------------------------------------------------------------

            # block to recognize "def"
            elif token == '' and char == 'd':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'd' and char == 'e':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'de' and char == 'f':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'def' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "def" and keep getting valid input, un-set the flag because we' now have an identifier
            elif token == 'def' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "main"
            # --------------------------------------------------------------------------
            elif token == '' and char == 'm':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'm' and char == 'a':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'ma' and char == 'i':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'mai' and char == 'n':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'main' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "main" and keep getting valid input, un-set the flag because we' now have an identifier
            elif token == 'main' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "read" or "return
            # -----------------------------------------------------------------------------
            elif token == '' and char == 'r':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'r' and char == 'e':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            # here is where the DFA divides - if we have "re" and get "a", we go down the "read" path.
            # if we have "re" and get "t" we go down the "return" path
            elif token == 're' and char == 'a':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'rea' and char == 'd':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'read' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "read" and keep getting valid input, un-set the flag because we' now have an identifier
            elif token == 'read' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to get the rest of the return keyword - branches off on line 264
            # -----------------------------------------------------------------------------
            elif token == 're' and char == 't':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'ret' and char == 'u':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'retu' and char == 'r':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'retur' and char == 'n':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'return' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "read" and keep getting valid input, un-set the flag because we' now have an identifier
            elif token == 'return' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "print"
            # --------------------------------------------------------------------------
            elif token == '' and char == 'p':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'p' and char == 'r':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'pr' and char == 'i':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'pri' and char == 'n':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'prin' and char == 't':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'print' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "print" and keep getting valid input, un-set the flag because we now have an identifier
            elif token == 'print' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "import" and "if
            # --------------------------------------------------------------------------
            elif token == '' and char == 'i':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            # dfa branches here - if our input is m, we take the "import" route, if it is F we take the "if" route
            elif token == 'i' and char == 'm':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'im' and char == 'p':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'imp' and char == 'o':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'impo' and char == 'r':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'impor' and char == 't':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'print' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "import" and keep getting valid input, un-set the flag because we have an identifier
            elif token == 'import' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to get the rest of the "if" keyword - branches off on line 337
            # -----------------------------------------------------------------------------
            elif token == 'i' and char == 'f':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'print' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "if" and keep getting valid input, un-set the flag because we now have an identifier
            elif token == 'if' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "global"
            # --------------------------------------------------------------------------
            elif token == '' and char == 'g':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'g' and char == 'l':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'gl' and char == 'o':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'glo' and char == 'b':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'glob' and char == 'a':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'globa' and char == 'l':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'global' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "global" and keep getting valid input, un-set the flag because we have an identifier
            elif token == 'global' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "break"
            # --------------------------------------------------------------------------
            elif token == '' and char == 'b':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'b' and char == 'r':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'br' and char == 'e':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'bre' and char == 'a':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'brea' and char == 'k':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'break' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "break" and keep getting valid input, un-set the flag because we now have an identifier
            elif token == 'break' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "continue"
            # --------------------------------------------------------------------------
            elif token == '' and char == 'c':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            # dfa branches here - if our input is m, we take the "import" route, if it is F we take the "if" route
            elif token == 'c' and char == 'o':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'co' and char == 'n':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'con' and char == 't':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'cont' and char == 'i':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'conti' and char == 'n':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'contin' and char == 'u':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'continu' and char == 'e':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'continue' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "continue" and keep getting valid input, un-set the flag because we have an identifier
            elif token == 'continue' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "else" and "elseif"
            # --------------------------------------------------------------------------
            elif token == '' and char == 'e':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'e' and char == 'l':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'el' and char == 's':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'els' and char == 'e':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'main' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "else" and keep getting valid input, un-set the flag because we' now have an identifier
            # we check if char != "i" here because an i would mean we have the elseif keyword
            # DFA branches here, elseif would continue on line 556
            elif token == 'else' and char != "i" and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize the rest of "elseif"
            # --------------------------------------------------------------------------
            elif token == 'else' and char == 'i':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'elsei' and char == 'f':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'elseif' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            elif token == 'elseif' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "while"
            # --------------------------------------------------------------------------
            elif token == '' and char == 'w':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'w' and char == 'h':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'wh' and char == 'i':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'whi' and char == 'l':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'whil' and char == 'e':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'while' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "while" and keep getting valid input, un-set the flag because we now have an identifier
            elif token == 'while' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "not"
            # -------------------------------------------------------------------------------
            elif token == '' and char == 'n':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'n' and char == 'o':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'no' and char == 't':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'def' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "def" and keep getting valid input, un-set the flag because we' now have an identifier
            elif token == 'not' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "true"
            # --------------------------------------------------------------------------
            elif token == '' and char == 't':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 't' and char == 'r':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'tr' and char == 'u':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'tru' and char == 'e':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'true' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "true" and keep getting valid input, un-set the flag because we' now have an identifier
            elif token == 'true' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "false"
            # --------------------------------------------------------------------------
            elif token == '' and char == 'f':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'f' and char == 'a':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'fa' and char == 'l':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'fal' and char == 's':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'fals' and char == 'e':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'false' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "false" and keep getting valid input, un-set the flag because we now have an identifier
            elif token == 'false' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "and"
            # -------------------------------------------------------------------------------
            elif token == '' and char == 'a':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'a' and char == 'n':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
            elif token == 'an' and char == 'd':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'and' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "and" and keep getting valid input, un-set the flag because we' now have an identifier
            elif token == 'and' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to recognize "or"
            # -------------------------------------------------------------------------------
            elif token == '' and char == 'o':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = True
            elif token == 'o' and char == 'r':
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isKey flag to true because we've found the 'def' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False
            # however, if we get "def" and keep getting valid input, un-set the flag because we' now have an identifier
            elif token == 'or' and (char.isalnum() or char == '.'):
                isKey = False
                # set the correct flag
                isID = True
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1

            # block to detect identifiers
            # ------------------------------------------------------------------------------------------------
            # the loop will only make it here if our character is a letter and is NOT the start of any keyword
            elif token == '' and char.isalpha():
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isID flag to True because we now have a identifier variable
                isID = True

            # recognizes the error case where an identifier starts with a   period
            elif token == '.' and (char.isalnum() or char == '.'):
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the appropriate error flag
                id_starting_decimal = True

            # if the identifier enters any of the keyword DFA states and fails out (in our context, fails the
            # appropriate elif) AND passes the error checks it will fall to here
            # this regex fails whenever the identifier doesn't contain the allowed symbols
            elif re.search('^[a-zA-Z0-9.]*$', token) and (char.isalnum() or char == '.'):
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the isID flag to True because we now have a identifier variable
                isID = True
                # set the isKey flag to false because we no longer have a keyword
                isKey = False

            # recognizes the error case where two identifiers are separated by an invalid special symbol.
            # all valid special symbols will be caught by the elif near the top, this case catches invalid ones
            elif not token.isalnum() or not char.isalnum():
                # add the current character to token
                token += char
                # increment our location on the line
                currchar += 1
                # set the appropriate error flag
                invalid_ss = True
                # turn the isId flag off because we no longer have an identifier
                isID = False

            else:
                print(token + " fell out of the world")


def BOOKKEEPER(token):
    global isID
    global isConst
    # pull in our global counter variable
    global table_row

    # our SYMTAB is a global variable, so we can just call for it here
    if table_row < 100:
        SYMTAB[table_row][0] = token  # first column is the symbol itself

        # assign proper type based on which flag has been set
        if isID:
            SYMTAB[table_row][1] = "ID"  # second column is type
        elif isConst:
            SYMTAB[table_row][1] = "Const"  # second column is type

        # increment the table_row counter so that we can move on down to the next row
        table_row = table_row + 1
    else:
        out_file = open('output.txt', 'a')
        out_file.write("Exceeded maximum SYMTAB size.\n")


def ERRORHANDLER(token):
    # pull in our global variables
    global invalid_const_two_decimals
    global invalid_ss
    global invalid_const_letter
    global const_starting_decimal
    global id_starting_decimal

    # open a filestream to write out the appropriate error
    out_file = open('output.txt', 'a')

    # prints the appropriate error message if a character is discovered that is not an approved special symbol
    if invalid_ss:
        out_file.write(token + " - Error: invalid special symbol\n")
    # prints the appropriate error message if a symbol we thought was a constant contains a letter
    elif invalid_const_letter:
        out_file.write(token + " - Error: constants cannot contain letters\n")
    # prints the appropriate error message if a symbol we thought was a constant contains > 1 decimals
    elif invalid_const_two_decimals:
        out_file.write(token + " - Error: constants may not contain more than one decimal point\n")
    elif const_starting_decimal:
        out_file.write(token + " - Error: constants cannot start with a decimal point\n")
    elif id_starting_decimal:
        out_file.write(token + " - Error: identifiers cannot start with a period\n")

    # close the output file
    out_file.close()


# small helper function that returns a boolean for the purpose of checking if constants are valid
def isFloat(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def toName(code_num):

    if code_num == 0:
        return "Z0"
    elif code_num == 1:
        return "[id]"
    elif code_num == 2:
        return "[const]"
    elif code_num == 3:
        return "def"
    elif code_num == 4:
        return "main"
    elif code_num == 5:
        return "read"
    elif code_num == 6:
        return "print"
    elif code_num == 7:
        return "import"
    elif code_num == 8:
        return "global"
    elif code_num == 9:
        return "break"
    elif code_num == 10:
        return "continue"
    elif code_num == 11:
        return "return"
    elif code_num == 12:
        return "if"
    elif code_num == 13:
        return "elseif"
    elif code_num == 14:
        return "else"
    elif code_num == 15:
        return "while"
    elif code_num == 16:
        return "not"
    elif code_num == 17:
        return "true"
    elif code_num == 18:
        return "false"
    elif code_num == 19:
        return "and"
    elif code_num == 20:
        return "or"
    elif code_num == 21:
        return ":"
    elif code_num == 22:
        return ","
    elif code_num == 23:
        return ";"
    elif code_num == 24:
        return "("
    elif code_num == 25:
        return ")"
    elif code_num == 26:
        return "["
    elif code_num == 27:
        return "]"
    elif code_num == 28:
        return "="
    elif code_num == 29:
        return "<"
    elif code_num == 30:
        return ">"
    elif code_num == 31:
        return "+"
    elif code_num == 32:
        return "*"
    elif code_num == 33:
        return "@"
    elif code_num == 34:
        return "<python>"
    elif code_num == 35:
        return "<def>"
    elif code_num == 36:
        return "<more-defs>"
    elif code_num == 37:
        return "<para-list>"
    elif code_num == 38:
        return "<block>"
    elif code_num == 39:
        return "<id-list>"
    elif code_num == 40:
        return "<more-ids>"
    elif code_num == 41:
        return "<stmts>"
    elif code_num == 42:
        return "<more-stmts>"
    elif code_num == 43:
        return "<stmt>"
    elif code_num == 44:
        return "<input>"
    elif code_num == 45:
        return "<output>"
    elif code_num == 46:
        return "<asmt>"
    elif code_num == 47:
        return "<expr-list>"
    elif code_num == 48:
        return "<expr>"
    elif code_num == 49:
        return "<more-exprs>"
    elif code_num == 50:
        return "<import>"
    elif code_num == 51:
        return "<global>"
    elif code_num == 52:
        return "<flow>"
    elif code_num == 53:
        return "<cond>"
    elif code_num == 54:
        return "<elseif>"
    elif code_num == 55:
        return "<elseif-list>"
    elif code_num == 56:
        return "<more-elseif>"
    elif code_num == 57:
        return "<else>"
    elif code_num == 58:
        return "<loop>"
    elif code_num == 59:
        return "<bool-expr>"
    elif code_num == 60:
        return "<bool>"
    elif code_num == 61:
        return "<comp>"
    elif code_num == 62:
        return "<arith-expr>"
    elif code_num == 63:
        return "<arith>"
    else:
        return "FAILED_TOKEN"


def outputWriter(steps, stack_top, lookahead, mode):

    # if  given the start symbol, we print out that we pushed the start symbol
    if mode == 'ss':
        return "Step: " + str(steps) + "  ---  Stack Top: " + toName(stack_top) + " (" + str(stack_top) + ")" +\
           "  ---  Lookahead: " + str(lookahead) + "  ---  Action: Pushed start symbol " + toName(NT_PYTHON) + " ("\
           + str(NT_PYTHON) + ")"
    # if expanding, we print out that we have expanded and say which rule we're using
    # (rule number will be appended in main)
    elif mode == 'expand':
        return "Step: " + str(steps) + "  ---  Stack Top: " + toName(stack_top) + " (" + str(stack_top) + ")" + \
               "  ---  Lookahead: " + str(lookahead) + "  ---  Action: Use Rule "
    # if the lookahead and stack top match, we accept and pop the token off the stack, and report accordingly
    elif mode == 'consume':
        return "Step: " + str(steps) + "  ---  Stack Top: " + toName(stack_top) + " (" + str(stack_top) + ")" + \
               "  ---  Lookahead: " + str(lookahead) + "  ---  Action: Matching"
    # if we see the stack bottom marker we know we can accept
    elif mode == "accept":
        return "Step: " + str(steps) + "  ---  Stack Top: " + toName(stack_top) + " (" + str(stack_top) + ")" + \
               "  ---  Lookahead: " + str(lookahead) + "  ---  Action: Accept"


if __name__ == "__main__":
    # run MAIN, which finds tokens, errors, and symbols and outputs them
    MAIN()
