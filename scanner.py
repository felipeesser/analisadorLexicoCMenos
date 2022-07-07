import util
from util import StateType, TokenType


class Scanner:
    def __init__(self, fileName):
        self.program = util.readFile(fileName)
        self.current_line = ''
        self.lineno = -1
        self.linepos = -1

    def __getNextLine(self):
        self.lineno += 1
        self.linepos = -1
        self.current_line = self.program[self.lineno]
        print(str(self.lineno + 1) + ": " + self.current_line)
        self.current_line += '\n'
        
    def getNextChar(self):
        try:
            self.linepos += 1
            return self.current_line[self.linepos]
        except: #Line completely read
            try:
                self.__getNextLine()
            except: #Program completely read
                return 'EOF'
            return self.getNextChar()

    def ungetNextChar(self):
        self.linepos -= 1

    def getToken(self):
        token_string = ''
        current_token = TokenType.ERROR
        state = StateType.START
        while not state == StateType.DONE:
            save = True
            c = self.getNextChar()
            if state == StateType.START:
                if c in [' ', '\n', '\t']:
                    save = False
                elif c == '>':
                    state = StateType.MAYBE_GREATER
                elif c == '<':
                    state = StateType.MAYBE_LESS
                elif c == '=':
                    state = StateType.MAYBE_EQ
                elif util.isLetter(c):
                    state = StateType.INID
                elif util.isDigit(c):
                    state = StateType.INNUM
                elif c == '!':
                    state = StateType.DIFF
                elif c == '/':
                    state = StateType.MAYBE_COMMENT
                else:
                    state = StateType.DONE
                    if c == '+':
                        current_token = TokenType.MAIS
                    elif c == '-':
                        current_token = TokenType.MENOS
                    elif c == '*':
                        current_token = TokenType.MULT
                    elif c == ';':
                        current_token = TokenType.PONTO_VIRGULA
                    elif c == ',':
                        current_token = TokenType.VIRGULA
                    elif c == '(':
                        current_token = TokenType.PARENT_OP
                    elif c == ')':
                        current_token = TokenType.PARENT_ED
                    elif c == '[':
                        current_token = TokenType.COLCH_OP
                    elif c == ']':
                        current_token = TokenType.COLCH_ED
                    elif c == '{':
                        current_token = TokenType.CHAVES_OP
                    elif c == '}':
                        current_token = TokenType.CHAVES_ED
                    elif c == 'EOF':
                        current_token = TokenType.EOF
            elif state == StateType.MAYBE_GREATER:
                state = StateType.DONE
                if c == '=':
                    current_token = TokenType.GREAT_EQUAL
                else:
                    current_token = TokenType.GREAT
                    self.ungetNextChar()
                    save = False
            elif state == StateType.MAYBE_LESS:
                state = StateType.DONE
                if c == '=':
                    current_token = TokenType.LESS_EQUAL
                else:
                    current_token = TokenType.LESS
                    self.ungetNextChar()
                    save = False
            elif state == StateType.MAYBE_EQ:
                state = StateType.DONE
                if c == '=':
                    current_token = TokenType.EQUAL
                else:
                    current_token = TokenType.ATTR
                    self.ungetNextChar()
                    save = False
            elif state == StateType.INID:
                if not util.isLetter(c):
                    self.ungetNextChar()
                    state = StateType.DONE
                    current_token = TokenType.ID
                    save = False
            elif state == StateType.INNUM:
                if not util.isDigit(c):
                    self.ungetNextChar()
                    state = StateType.DONE
                    current_token = TokenType.NUM
                    save = False
            elif state == StateType.DIFF:
                state = StateType.DONE
                if c == '=':
                    current_token = TokenType.DIF
                else:
                    current_token = TokenType.ERROR
                    self.ungetNextChar()
                    save = False
            elif state == StateType.MAYBE_COMMENT:
                if c == '*':
                    state = StateType.COMMENT
                else:
                    self.ungetNextChar()
                    state = StateType.DONE
                    current_token = TokenType.DIV
                    save = False
            elif state == StateType.COMMENT:
                if c == '*':
                    state = StateType.INCOMMENT
                elif c == 'EOF':
                    state = StateType.DONE
                    current_token = TokenType.EOF
            elif state == StateType.INCOMMENT:
                if c == '/':
                    state = StateType.START
                    token_string = ''
                    save = False
                elif c == 'EOF':
                    state = StateType.DONE
                    current_token = TokenType.EOF
                else:
                    state = StateType.COMMENT
            if save:
                token_string += c
        if current_token == TokenType.ID:
            current_token = util.reservedLookup(token_string)
        util.printToken(current_token, token_string, self.lineno+1)
        return [current_token,token_string]
