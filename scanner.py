import util
from util import StateType, TokenType


class Scanner:
    def __init__(self, fileName):
        self.program = util.readFile(fileName)
        self.current_line = ''
        self.lineno = 0
        self.linepos = 0

    def getNextChar(self):
        self.linepos += 1
        if not self.linepos < len(self.current_line):
            self.lineno += 1
            if self.lineno - 1 < len(self.program):
                self.current_line = self.program[self.lineno - 1]
                print(str(self.lineno) + ": " + self.current_line)
                self.linepos = 0
                if self.current_line == '':
                    return self.getNextChar()
                return self.current_line[self.linepos]
            else:
                return 'EOF'
        else:
            return self.current_line[self.linepos]

    def ungetNextChar(self):
        self.linepos -= 1

    def getToken(self):
        token_string = ''
        current_token = TokenType.OTHER
        state = StateType.START
        while not state == StateType.DONE:
            save = True
            c = self.getNextChar()
            if state == StateType.START:
                if c == ' ':
                    save = False
                elif util.isLetter(c):
                    state = StateType.INID
                elif util.isDigit(c):
                    state = StateType.INNUM
                elif c == '/':
                    state = StateType.MAYBE_COMMENT
                else:
                    state = StateType.DONE
                    if c == ';':
                        current_token = TokenType.PONTO_VIRGULA
                    elif c == '+':
                        current_token = TokenType.MAIS
                    elif c == '-':
                        current_token = TokenType.MENOS
                    elif c == '*':
                        current_token = TokenType.MULT
                    elif c == '(':
                        current_token = TokenType.PARENT_OP
                    elif c == ')':
                        current_token = TokenType.PARENT_ED
                    elif c == '{':
                        current_token = TokenType.CHAVES_OP
                    elif c == '}':
                        current_token = TokenType.CHAVES_ED
                    elif c == '[':
                        current_token = TokenType.COLCH_OP
                    elif c == ']':
                        current_token = TokenType.COLCH_ED
                    elif c == ',':
                        current_token = TokenType.VIRGULA
                    elif c == 'EOF':
                        current_token = TokenType.EOF
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
        util.printToken(current_token, token_string, self.lineno)
        return current_token
