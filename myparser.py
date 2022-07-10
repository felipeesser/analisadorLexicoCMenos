from TreeNode import TreeNode
from util import TokenType


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.token = None
        self.prevToken = [None, None, None]
        self.identifiers_table = [[]]

    def match(self, expectedToken):
        if self.token[0] == expectedToken:
            self.token = self.scanner.getToken()
        else:
            self.error(expectedToken)

    def error(self, expectedToken):
        print(f'Erro na linha {self.token[2]} : Esperando token {expectedToken.name} no lugar de {self.token[1]}')
        exit(1)

    def parse(self):
        self.token = self.scanner.getToken()
        return self.program()

    def program(self):
        return self.declaration_list()

    def declaration_list(self):
        t = self.declaration()
        p = t
        while self.token[0] == TokenType.INT or self.token[0] == TokenType.VOID:
            q = self.declaration()
            p.sibling = q
            p = q
        return t

    def declaration(self):
        t = TreeNode()
        t.children.append(self.type_specifier())
        id_node = TreeNode()
        id_node.type = 'ID'
        id_node.attr = self.token[1]
        self.match(TokenType.ID)
        t.children.append(id_node)
        if self.token[0] == TokenType.PARENT_OP:  # fun_declaration
            self.identifiers_table.append(self.identifiers_table[-1].copy())
            self.match(TokenType.PARENT_OP)
            p = self.params()
            params = []
            for param in p.children:
                params.append(param.children[1].attr)
            self.match(TokenType.PARENT_ED)
            t.children.append(p)
            self.identifiers_table[-1] += params
            t.children.append(self.compound_stmt())
            t.type = 'FUN-DECLARATION'
            self.identifiers_table.pop()
        else:  # var_declaration
            if self.token[0] == TokenType.COLCH_OP:
                self.match(TokenType.COLCH_OP)
                self.match(TokenType.NUM)
                self.match(TokenType.COLCH_ED)
            self.match(TokenType.PONTO_VIRGULA)
            t.type = 'VAR-DECLARATION'
            self.identifiers_table[-1].append(id_node.attr)
        return t

    def type_specifier(self):
        t = TreeNode()
        t.type = 'TYPE-SPECIFIER'
        if self.token[0] == TokenType.INT:
            self.match(TokenType.INT)
            t.attr = 'int'
        elif self.token[0] == TokenType.VOID:
            self.match(TokenType.VOID)
            t.attr = 'void'
        return t

    def params(self):
        t = TreeNode()
        t.type = 'PARAMS'
        if self.token[0] == TokenType.VOID:
            self.match(TokenType.VOID)
        else:
            t.children += self.param_list()
        return t

    def param_list(self):
        params = []
        t = self.param()
        params.append(t)
        while self.token[0] == TokenType.VIRGULA:
            self.match(TokenType.VIRGULA)
            q = self.param()
            params.append(q)
        return params

    def param(self):
        t = TreeNode()
        t.children.append(self.type_specifier())
        id_node = TreeNode()
        id_node.type = 'ID'
        id_node.attr = self.token[1]
        self.match(TokenType.ID)
        t.children.append(id_node)
        t.attr = self.token[1]
        if self.token[0] == TokenType.COLCH_OP:
            self.match(TokenType.COLCH_OP)
            self.match(TokenType.COLCH_ED)
        t.type = 'PARAM'
        return t

    def compound_stmt(self):
        t = TreeNode()
        t.type = 'COMPOUND-STMT'
        self.match(TokenType.CHAVES_OP)
        self.identifiers_table.append(self.identifiers_table[-1].copy())
        t.children += self.local_declarations()
        t.children += self.statement_list()
        self.match(TokenType.CHAVES_ED)
        self.identifiers_table.pop()
        return t

    def local_declarations(self):
        # var_declaration
        declarations = []
        while self.token[0] == TokenType.INT or self.token[0] == TokenType.VOID:
            t = TreeNode()
            t.type = 'VAR-DECLARATION'
            t.children.append(self.type_specifier())
            id_node = TreeNode()
            id_node.type = 'ID'
            id_node.attr = self.token[1]
            self.match(TokenType.ID)
            t.children.append(id_node)
            self.identifiers_table[-1].append(id_node.attr)
            if self.token[0] == TokenType.COLCH_OP:
                self.match(TokenType.COLCH_OP)
                self.match(TokenType.NUM)
                self.match(TokenType.COLCH_ED)
            self.match(TokenType.PONTO_VIRGULA)
            declarations.append(t)
        return declarations

    def statement_list(self):
        statements = []
        while (self.token[0] == TokenType.PONTO_VIRGULA or self.token[0] == TokenType.ID or
               self.token[0] == TokenType.PARENT_OP or self.token[0] == TokenType.NUM or
               self.token[0] == TokenType.RETURN or self.token[0] == TokenType.CHAVES_OP or
               self.token[0] == TokenType.IF or self.token[0] == TokenType.WHILE):
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.token[0] == TokenType.RETURN:
            return self.return_stmt()
        elif self.token[0] == TokenType.CHAVES_OP:
            self.compound_stmt()
        elif self.token[0] == TokenType.IF:
            return self.selection_stmt()
        elif self.token[0] == TokenType.WHILE:
            return self.iteration_stmt()
        else:
            return self.expression_stmt()

    def selection_stmt(self):
        t = TreeNode()
        t.type = 'SELECTION-STMT'
        self.match(TokenType.IF)
        self.match(TokenType.PARENT_OP)
        t.children.append(self.expression())
        self.match(TokenType.PARENT_ED)
        t.children.append(self.statement())
        if self.token[0] == TokenType.ELSE:
            self.match(TokenType.ELSE)
            t.children.append(self.statement())
        return t

    def iteration_stmt(self):
        t = TreeNode()
        t.type = 'ITERATION-STMT'
        self.match(TokenType.WHILE)
        self.match(TokenType.PARENT_OP)
        t.children.append(self.expression())
        self.match(TokenType.PARENT_ED)
        t.children.append(self.statement())
        return t

    def return_stmt(self):
        t = TreeNode()
        t.type = 'RETURN-STMT'
        self.match(TokenType.RETURN)
        if (self.token[0] == TokenType.PONTO_VIRGULA or self.token[0] == TokenType.ID or
                self.token[0] == TokenType.PARENT_OP or self.token[0] == TokenType.NUM):
            t.children.append(self.expression())
        self.match(TokenType.PONTO_VIRGULA)
        return t

    def expression_stmt(self):
        t = TreeNode()
        t.type = 'EXPRESSION-STMT'
        if (self.token[0] == TokenType.PONTO_VIRGULA or self.token[0] == TokenType.ID or
                self.token[0] == TokenType.PARENT_OP or self.token[0] == TokenType.NUM):
            t.children.append(self.expression())
        self.match(TokenType.PONTO_VIRGULA)
        return t

    def expression(self):
        t = TreeNode()
        t.type = 'EXPRESSION'
        p = t
        while self.token[0] == TokenType.ID:
            q = TreeNode()
            q.attr = self.token[1]
            prev_token = self.token
            id_line = self.token[2]
            self.match(TokenType.ID)
            if self.token[0] == TokenType.COLCH_OP:
                self.match(TokenType.COLCH_OP)
                q.children.append(self.expression())
                self.match(TokenType.COLCH_ED)
                if self.token[0] == TokenType.ATTR:
                    self.match(TokenType.ATTR)
            else:
                if self.token[0] == TokenType.ATTR:
                    self.match(TokenType.ATTR)
                else:
                    self.prevToken = prev_token
                    break
            q.type = 'ASSIGN'
            p.children.append(q)
            p = q
            available_vars = self.identifiers_table[-1]
            if p.attr not in available_vars:
                print(f'Erro na linha {id_line}: Variável {p.attr} sendo utilizada antes de sua declaração')
                exit(1)
        p.children.append(self.simple_expression())
        return t

    def simple_expression(self):
        t = TreeNode()
        t.type = 'SIMPLE-EXPRESSION'
        t.children.append(self.additive_expression())
        if (self.token[0] == TokenType.GREAT or self.token[0] == TokenType.GREAT_EQUAL or
                self.token[0] == TokenType.EQUAL or self.token[0] == TokenType.LESS or
                self.token[0] == TokenType.LESS_EQUAL or self.token[0] == TokenType.DIF):
            t.children.append(self.relop())
            t.children.append(self.additive_expression())
        return t

    def relop(self):
        t = TreeNode()
        t.type = 'RELOP'
        if self.token[0] == TokenType.GREAT:
            t.attr = '>'
            self.match(TokenType.GREAT)
        elif self.token[0] == TokenType.GREAT_EQUAL:
            t.attr = '>='
            self.match(TokenType.GREAT_EQUAL)
        elif self.token[0] == TokenType.EQUAL:
            t.attr = '=='
            self.match(TokenType.EQUAL)
        elif self.token[0] == TokenType.LESS:
            t.attr = '<'
            self.match(TokenType.LESS)
        elif self.token[0] == TokenType.LESS_EQUAL:
            t.attr = '<='
            self.match(TokenType.LESS_EQUAL)
        elif self.token[0] == TokenType.DIF:
            t.attr = '!='
            self.match(TokenType.DIF)
        return t

    def additive_expression(self):
        t = TreeNode()
        t.type = 'ADDITIVE-EXPRESSION'
        t.children.append(self.term())
        if self.token[0] == TokenType.MAIS or self.token[0] == TokenType.MENOS:
            t.children.append(self.addop())
            t.children.append(self.term())
        return t

    def addop(self):
        t = TreeNode()
        t.type = 'ADDOP'
        if self.token[0] == TokenType.MAIS:
            t.attr = '+'
            self.match(TokenType.MAIS)
        elif self.token[0] == TokenType.MENOS:
            t.attr = '-'
            self.match(TokenType.MENOS)
        return t

    def term(self):
        t = TreeNode()
        t.type = 'TERM'
        t.children.append(self.factor())
        while self.token[0] == TokenType.MULT or self.token[0] == TokenType.DIV:
            t.children.append(self.mulop())
            t.children.append(self.factor())
        return t

    def mulop(self):
        t = TreeNode()
        t.type = 'MULOP'
        if self.token[0] == TokenType.MULT:
            t.attr = '*'
            self.match(TokenType.MULT)
        elif self.token[0] == TokenType.DIV:
            t.attr = '/'
            self.match(TokenType.DIV)
        return t

    def factor(self):
        t = TreeNode()
        t.type = 'FACTOR'
        if self.token[0] == TokenType.ID or self.prevToken[0] == TokenType.ID:
            p = TreeNode()
            id_line = self.prevToken[2]
            p.attr = self.prevToken[1]
            if not self.prevToken[0] == TokenType.ID:
                p.attr = self.token[1]
                id_line = self.token[2]
                self.match(TokenType.ID)
            self.prevToken = [None, None, None]
            if self.token[0] == TokenType.PARENT_OP:  # call
                p.type = 'CALL'
                self.match(TokenType.PARENT_OP)
                p.children.append(self.args())
                self.match(TokenType.PARENT_ED)
            else:  # var
                p.type = 'VAR'
                if self.token[0] == TokenType.COLCH_OP:
                    self.match(TokenType.COLCH_OP)
                    p.children.append(self.expression())
                    self.match(TokenType.COLCH_ED)
                available_vars = self.identifiers_table[-1]
                if p.attr not in available_vars:
                    print(f'Erro na linha {id_line}: Variável {p.attr} sendo utilizada antes de sua declaração')
                    exit(1)
            t.children.append(p)
        elif self.token[0] == TokenType.PARENT_OP:
            self.match(TokenType.PARENT_OP)
            t.children.append(self.expression())
            self.match(TokenType.PARENT_ED)
        elif self.token[0] == TokenType.NUM:
            p = TreeNode()
            p.type = 'NUM'
            p.attr = self.token[1]
            t.children.append(p)
            self.match(TokenType.NUM)
        return t

    def args(self):
        t = TreeNode()
        t.type = 'ARGS'
        t.children.append(self.expression())
        while self.token[0] == TokenType.VIRGULA:
            self.match(TokenType.VIRGULA)
            t.children.append(self.expression())
        return t
