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


def MAIN():
    # read in input file
    in_file = open('input.txt', 'r')

    # store in a variable so we can pass it to main
    input = in_file.read()

    # write input file to our big output file
    out_file = open('output.txt', 'w')
    out_file.write(input + "\n\n")
    # close output file, since all writing after this should be appended to the end of the file
    out_file.close()

    # loop through until input is empty
    while input != None:
        # every time a token is discovered or white space is ignored, we print it and return the shortened string
        input = SCANNER(input)

    # print our symtab table
    out_file = open('output.txt', 'a')
    out_file.write("\n\n")
    for row in SYMTAB:
        out_file.write(str(row) + "\n")
    # close the output file
    out_file.close()


def SCANNER(input):
    # pull our global variables into the function
    global isKey
    global isID
    global isConst
    global invalid_const_two_decimals
    global invalid_ss
    global invalid_const_letter
    global const_starting_decimal
    global id_starting_decimal

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
            print("token: " + repr(token) + " char: " + repr(char))
            # block to recognize comments
            # -----------------------------------------------------------------------------------------------
            if char == '#':
                # write the # out to the file
                outfile = open('output.txt', 'a')
                outfile.write(char + " - " + 'Special Symbol\n')
                outfile.close()
                # remove whatever is left of the line (aka the comment) from our input string
                comment_length = len(line) - currchar
                input = input[comment_length:]
                # break out of the loop for this line and get a new one
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

                    if isKey:
                        outfile = open('output.txt', 'a')
                        outfile.write(token + " - " + 'Keyword\n')
                        outfile.close()
                    elif isConst:
                        # check symtab to see if we've already put it in there
                        for row in range(100):
                            if SYMTAB[row][0] == token:
                                is_in_table = True
                        # if the symbol is not in the symtab, put it in there
                        if not is_in_table:
                            BOOKKEEPER(token)
                        # write the symbol out to our output file
                        outfile = open('output.txt', 'a')
                        outfile.write(token + " - " + 'Constant\n')
                        outfile.close()
                    elif isID:
                        # check symtab to see if we've already put it in there
                        for row in range(100):
                            if SYMTAB[row][0] == token:
                                is_in_table = True
                        # if the symbol is not in the symtab, put it in there
                        if not is_in_table:
                            print("bookkept token: " + token + " when char: " + char + ".")
                            BOOKKEEPER(token)
                        # write the symbol out to our output file
                        outfile = open('output.txt', 'a')
                        outfile.write(token + " - " + 'Identifier\n')
                        outfile.close()
                    # then, if our delimiter is a special symbol, write it to the output file as well
                    if char != ' ' and char != "\n" and char != '':
                        outfile = open('output.txt', 'a')
                        outfile.write(char + " - " + 'Special Symbol\n')
                        outfile.close()
                # if there is an error, call the error handler on it
                else:
                    ERRORHANDLER(token)
                    # then, if our delimiter is a special symbol, write it to the output file as well
                    if char != ' ' and char != "\n" and char != '':
                        outfile = open('output.txt', 'a')
                        outfile.write(char + " - " + 'Special Symbol\n')
                        outfile.close()

                # lastly, remove the token and special symbol from input and return it
                token_and_ss = len(token) + 1
                return input[token_and_ss:]

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
                # set the isKey flag to true because we've found the 'main' keyword
                isKey = True
                # we set it as an ID to start with and only change that if it is proven to be a keyword
                isID = False

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
                print("id flag set for token: " + token +" and char: " + char + ".")
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
                print("id flag turned off for token: " + token + " and char: " + char + ".")
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
        # print("token: " + str(token) + " id: " + str(isID) + " const: " + str(isConst))
        SYMTAB[table_row][0] = token  # first column is the symbol itself

        # assign proper type based on which flag has been set
        if isID:
            SYMTAB[table_row][1] = "ID"  # second column is type
        elif isConst:
            SYMTAB[table_row][1] = "Const"  # second column is type

        # increment the table_row counter so that we can move on down to the next row
        table_row = table_row + 1
    else:
        print("table too big")


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


if __name__ == "__main__":
    # run MAIN, which finds tokens, errors, and symbols and outputs them
    MAIN()
