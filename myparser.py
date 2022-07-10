from TreeNode import TreeNode
from util import TokenType


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.token = None
        self.prevToken = None

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
            self.match(TokenType.PARENT_OP)
            t.children.append(self.params())
            self.match(TokenType.PARENT_ED)
            self.compound_stmt()
            t.type = 'FUN-DECLARATION'
        else:  # var_declaration
            if self.token[0] == TokenType.COLCH_OP:
                self.match(TokenType.COLCH_OP)
                self.match(TokenType.NUM)
                self.match(TokenType.COLCH_ED)
            self.match(TokenType.PONTO_VIRGULA)
            t.type = 'VAR-DECLARATION'
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
            t.children.append(self.param_list())
        return t

    def param_list(self):
        params = []
        t = self.param()
        p = t
        params.append(t)
        while self.token[0] == TokenType.VIRGULA:
            self.match(TokenType.VIRGULA)
            q = self.param()
            p.sibling = q
            p = q
            params.append(q)
        return t

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
        self.match(TokenType.CHAVES_OP)
        self.local_declarations()
        self.statement_list()
        self.match(TokenType.CHAVES_ED)

    def local_declarations(self):
        # var_declaration
        while self.token[0] == TokenType.INT or self.token[0] == TokenType.VOID:
            self.type_specifier()
            self.match(TokenType.ID)
            if self.token[0] == TokenType.COLCH_OP:
                self.match(TokenType.COLCH_OP)
                self.match(TokenType.NUM)
                self.match(TokenType.COLCH_ED)
            self.match(TokenType.PONTO_VIRGULA)

    def statement_list(self):
        while (self.token[0] == TokenType.PONTO_VIRGULA or self.token[0] == TokenType.ID or
               self.token[0] == TokenType.PARENT_OP or self.token[0] == TokenType.NUM or
               self.token[0] == TokenType.RETURN or self.token[0] == TokenType.CHAVES_OP or
               self.token[0] == TokenType.IF or self.token[0] == TokenType.WHILE):
            self.statement()

    def statement(self):
        if self.token[0] == TokenType.RETURN:
            self.return_stmt()
        elif self.token[0] == TokenType.CHAVES_OP:
            self.compound_stmt()
        elif self.token[0] == TokenType.IF:
            self.selection_stmt()
        elif self.token[0] == TokenType.WHILE:
            self.iteration_stmt()
        else:
            self.expression_stmt()

    def selection_stmt(self):
        self.match(TokenType.IF)
        self.match(TokenType.PARENT_OP)
        self.expression()
        self.match(TokenType.PARENT_ED)
        self.statement()
        if self.token[0] == TokenType.ELSE:
            self.match(TokenType.ELSE)
            self.statement()

    def iteration_stmt(self):
        self.match(TokenType.WHILE)
        self.match(TokenType.PARENT_OP)
        self.expression()
        self.match(TokenType.PARENT_ED)
        self.statement()

    def return_stmt(self):
        self.match(TokenType.RETURN)
        if (self.token[0] == TokenType.PONTO_VIRGULA or self.token[0] == TokenType.ID or
                self.token[0] == TokenType.PARENT_OP or self.token[0] == TokenType.NUM):
            self.expression()
        self.match(TokenType.PONTO_VIRGULA)

    def expression_stmt(self):
        if (self.token[0] == TokenType.PONTO_VIRGULA or self.token[0] == TokenType.ID or
                self.token[0] == TokenType.PARENT_OP or self.token[0] == TokenType.NUM):
            self.expression()
        self.match(TokenType.PONTO_VIRGULA)

    def expression(self):
        while self.token[0] == TokenType.ID:
            self.match(TokenType.ID)
            if self.token[0] == TokenType.COLCH_OP:
                self.match(TokenType.COLCH_OP)
                self.expression()
                self.match(TokenType.COLCH_ED)
                self.match(TokenType.ATTR)
            else:
                if self.token[0] == TokenType.ATTR:
                    self.match(TokenType.ATTR)
                else:
                    break
        self.prevToken = TokenType.ID
        self.simple_expression()

    def var(self):
        self.match(TokenType.ID)
        if self.token[0] == TokenType.COLCH_OP:
            self.match(TokenType.COLCH_OP)
            self.expression()
            self.match(TokenType.COLCH_ED)

    def simple_expression(self):
        self.additive_expression()
        if (self.token[0] == TokenType.GREAT or self.token[0] == TokenType.GREAT_EQUAL or
                self.token[0] == TokenType.EQUAL or self.token[0] == TokenType.LESS or
                self.token[0] == TokenType.LESS_EQUAL or self.token[0] == TokenType.DIF):
            self.relop()
            self.additive_expression()

    def relop(self):
        if self.token[0] == TokenType.GREAT:
            self.match(TokenType.GREAT)
        elif self.token[0] == TokenType.GREAT_EQUAL:
            self.match(TokenType.GREAT_EQUAL)
        elif self.token[0] == TokenType.EQUAL:
            self.match(TokenType.EQUAL)
        elif self.token[0] == TokenType.LESS:
            self.match(TokenType.LESS)
        elif self.token[0] == TokenType.LESS_EQUAL:
            self.match(TokenType.LESS_EQUAL)
        elif self.token[0] == TokenType.DIF:
            self.match(TokenType.DIF)

    def additive_expression(self):
        self.term()
        if self.token[0] == TokenType.MAIS or self.token[0] == TokenType.MENOS:
            self.addop()
            self.term()

    def addop(self):
        if self.token[0] == TokenType.MAIS:
            self.match(TokenType.MAIS)
        elif self.token[0] == TokenType.MENOS:
            self.match(TokenType.MENOS)

    def term(self):
        self.factor()
        while self.token[0] == TokenType.MULT or self.token[0] == TokenType.DIV:
            self.mulop()
            self.factor()

    def mulop(self):
        if self.token[0] == TokenType.MULT:
            self.match(TokenType.MULT)
        elif self.token[0] == TokenType.DIV:
            self.match(TokenType.DIV)

    def factor(self):
        if self.token[0] == TokenType.ID or self.prevToken == TokenType.ID:
            if not self.prevToken == TokenType.ID:
                self.match(TokenType.ID)
            self.prevToken = None
            if self.token[0] == TokenType.PARENT_OP:  # call
                self.match(TokenType.PARENT_OP)
                self.args()
                self.match(TokenType.PARENT_ED)
            else:  # var
                if self.token[0] == TokenType.COLCH_OP:
                    self.match(TokenType.COLCH_OP)
                    self.expression()
                    self.match(TokenType.COLCH_ED)
        elif self.token[0] == TokenType.PARENT_OP:
            self.match(TokenType.PARENT_OP)
            self.expression()
            self.match(TokenType.PARENT_ED)
        elif self.token[0] == TokenType.NUM:
            self.match(TokenType.NUM)

    def args(self):
        self.expression()
        while self.token[0] == TokenType.VIRGULA:
            self.match(TokenType.VIRGULA)
            self.expression()
