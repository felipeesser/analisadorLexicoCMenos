import util


class Scanner:
    ESTADOS = {'start': False, 'end': False, 'other': False, 'inid': False, 'inmult': False, 'indiv': False,
               'innum': False, 'maybecomment': False, 'comment': False, 'incomment': False}

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

    def setEstado(self, estado):
        for e in self.ESTADOS:
            self.ESTADOS[e] = False
        self.ESTADOS[estado] = True

    def getEstado(self, estado):
        return self.ESTADOS[estado]

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
        self.setEstado('start')
        while not self.getEstado('end'):
            save = True
            c = self.getNextChar()
            if self.getEstado('start'):
                if c == ' ':
                    save = False
                elif util.isLetter(c):
                    self.setEstado('inid')
                elif util.isDigit(c):
                    self.setEstado('innum')
                elif c == '/':
                    self.setEstado('maybecomment')
                else:
                    self.setEstado('end')
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
            elif self.getEstado('inid'):
                if not util.isLetter(c) or c == 'EOF':
                    self.ungetNextChar()
                    self.setEstado('end')
                    current_token = 'ID'
                    save = False
            elif self.getEstado('innum'):
                if not util.isDigit(c) or c == 'EOF':
                    self.ungetNextChar()
                    self.setEstado('end')
                    current_token = 'NUM'
                    save = False
            elif self.getEstado('maybecomment'):
                if c == '*':
                    self.setEstado('comment')
                else:
                    self.ungetNextChar()
                    self.setEstado('end')
                    current_token = 'div'
                    save = False
            elif self.getEstado('comment'):
                if c == '*':
                    self.setEstado('incomment')
            elif self.getEstado('incomment'):
                if c == '/':
                    self.setEstado('start')
                    token_string = ''
                    save = False
                else:
                    self.setEstado('incomment')
            if save:
                token_string += c
            if token_string == 'EOF':
                current_token = 'EOF'
                break
        if current_token == 'ID':
            current_token = util.reservedLookup(token_string)
        print('    ' + str(self.lineno) + ': ' + current_token + ', ' + token_string)
        return current_token
