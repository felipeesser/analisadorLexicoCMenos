import util
from util import StateType


class Scanner:
    OPERADORES = {
        '+': 'add',
        '-': 'minus',
        '*': 'mult',
        '/': 'div',
        '<': 'menor',
        '<=': '',
        '>': 'maior',
        '>=': '',
        '==': '',
        '!=': '',
        '=': 'attr',
        ';': 'pontovirgula',
        ',': 'virgula',
        '(': 'parentop',
        ')': 'parented',
        '[': 'colcheop',
        ']': 'colcheed',
        '{': 'chavesop',
        '}': 'chavesed',
        '/*': 'opcomment',
        '*/': 'endcomment'
    }

    def __init__(self, nomeArquivo):
        self.tokens = []
        self.programa = util.readFile(nomeArquivo)
        self.current_line = ''
        self.lineno = 0
        self.linepos = 0

    def getNextChar(self):
        self.linepos += 1
        if not self.linepos < len(self.current_line):
            self.lineno += 1
            if self.lineno - 1 < len(self.programa):
                self.current_line = self.programa[self.lineno - 1]
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
        current_token = 'other'
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
                        current_token = 'pontovirgula'
                    elif c == '+':
                        current_token = 'add'
                    elif c == '-':
                        current_token = 'minus'
                    elif c == '*':
                        current_token = 'mult'
                    elif c == '(':
                        current_token = 'parentop'
                    elif c == ')':
                        current_token = 'parented'
                    elif c == '{':
                        current_token = 'chavesop'
                    elif c == '}':
                        current_token = 'chavesed'
                    elif c == '[':
                        current_token = 'colcheop'
                    elif c == ']':
                        current_token = 'colcheed'
                    elif c == ',':
                        current_token = 'virgula'
            elif state == StateType.INID:
                if not util.isLetter(c) or c == 'EOF':
                    self.ungetNextChar()
                    state = StateType.DONE
                    current_token = 'ID'
                    save = False
            elif state == StateType.INNUM:
                if not util.isDigit(c) or c == 'EOF':
                    self.ungetNextChar()
                    state = StateType.DONE
                    current_token = 'NUM'
                    save = False
            elif state == StateType.MAYBE_COMMENT:
                if c == '*':
                    state = StateType.COMMENT
                else:
                    self.ungetNextChar()
                    state = StateType.DONE
                    current_token = 'div'
                    save = False
            elif state == StateType.COMMENT:
                if c == '*':
                    state = StateType.INCOMMENT
            elif state == StateType.INCOMMENT:
                if c == '/':
                    state = StateType.START
                    token_string = ''
                    save = False
                else:
                    state = StateType.INCOMMENT
            if save:
                token_string += c
            if token_string == 'EOF':
                current_token = 'EOF'
                break
        if current_token == 'ID':
            current_token = util.reservedLookup(token_string)
        print('    ' + str(self.lineno) + ': ' + current_token + ', ' + token_string)
        return current_token
