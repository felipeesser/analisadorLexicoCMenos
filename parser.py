from ast import If
from scanner import Scanner
from util import TokenType


class Parser:
    def __init__(self, filename):
        self.scanner = Scanner(filename)
        self.token=self.scanner.getToken()
    def error(self):
        print(self.token[0].name,self.token[1],self.token[2])
        if(self.token[0]==TokenType.EOF):
            exit(1)
        print('erro')
        exit(1)
    def match(self,expectedToken):
        if (self.token[0]==expectedToken):
            self.token=self.scanner.getToken()
        else:
            self.error()
    def addop(self):
        if(self.token[0]==TokenType.MAIS):
            self.match(TokenType.MAIS)
        elif(self.token[0]==TokenType.MENOS):
            self.match(TokenType.MENOS)
        else:
            self.error()
    def additive_expression(self):
        if(self.token[0]==TokenType.NUM or self.token[0]==TokenType.PARENT_OP):
            self.term()
            self.additive_expression_()
        else:
            self.error()
    def additive_expression_(self):
        if(self.token[0]==TokenType.MAIS or self.token[0]==TokenType.MENOS):
            self.addop()
            self.term()
            self.additive_expression_()
    def mulop(self):
        if(self.token[0]==TokenType.MULT):
            self.match(TokenType.MULT)
        elif(self.token[0]==TokenType.DIV):
            self.match(TokenType.DIV) 
        else:
            self.error() 
    def term(self):
        if(self.token[0]==TokenType.NUM or self.token[0]==TokenType.PARENT_OP):
            self.factor()
            self.term_()
        else:
            self.error()
    def term_(self):
        if(self.token[0]==TokenType.MULT or self.token[0]==TokenType.DIV):
            self.mulop()
            self.factor()
            self.term_()
    def relop(self):
        if(self.token[0]==TokenType.GREAT):
            self.match(TokenType.GREAT)
        elif(self.token[0]==TokenType.GREAT_EQUAL):
            self.match(TokenType.GREAT_EQUAL)
        elif(self.token[0]==TokenType.EQUAL):
            self.match(TokenType.EQUAL)
        elif(self.token[0]==TokenType.LESS):
            self.match(TokenType.LESS)
        elif(self.token[0]==TokenType.LESS_EQUAL):
            self.match(TokenType.LESS_EQUAL)
        elif(self.token[0]==TokenType.DIF):
            self.match(TokenType.DIF)
        else:
            self.error() 
    def relop_(self):
        if(self.token[0]==TokenType.GREAT or self.token[0]==TokenType.GREAT_EQUAL or self.token[0]==TokenType.EQUAL 
        or self.token[0]==TokenType.LESS or self.token[0]==TokenType.LESS_EQUAL or self.token[0]==TokenType.DIF):
            self.relop()
            self.additive_expression()
    def simple_expression(self):
        if(self.token[0]==TokenType.NUM or self.token[0]==TokenType.PARENT_OP):
            self.additive_expression()
            self.relop_()
        else:
            self.error()
    def expression(self):
        if(self.token[0]==TokenType.NUM or self.token[0]==TokenType.PARENT_OP):
            self.simple_expression()
        else:
            self.error()
    def expression_(self):
        if(self.token[0]==TokenType.PONTO_VIRGULA):
            self.match(TokenType.PONTO_VIRGULA)
        elif(self.token[0]==TokenType.NUM or self.token[0]==TokenType.PARENT_OP):
            self.expression()
            self.match(TokenType.PONTO_VIRGULA)
        else:
            self.error()
    def return_stmt(self):
        if(self.token[0]==TokenType.RETURN):
            self.match(TokenType.RETURN)
            self.expression_()
        else:
            self.error()
    def iteration_stmt(self):
        if(self.token[0]==TokenType.WHILE):
            self.match(TokenType.WHILE)
            self.match(TokenType.PARENT_OP)
            self.expression()
            self.match(TokenType.PARENT_ED)
            self.statement()
        else:
            self.error()
    def selection_stmt(self):
        if(self.token[0]==TokenType.IF):
            self.match(TokenType.IF)
            self.match(TokenType.PARENT_OP)
            self.expression()
            self.match(TokenType.PARENT_ED)
            self.statement()
            self.else_()
        else:
            self.error()
    def else_(self):
        if(self.token[0]==TokenType.ELSE):
            self.match(TokenType.ELSE)
            self.statement()
    def statement_list(self):
        if(self.token[0]==TokenType.WHILE or self.token[0]==TokenType.RETURN or self.token[0]==TokenType.IF or 
        self.token[0]==TokenType.PONTO_VIRGULA or self.token[0]==TokenType.NUM or self.token[0]==TokenType.PARENT_OP or 
        self.token[0]==TokenType.CHAVES_OP):
            self.statement_list_()
    def statement_list_(self):
        if(self.token[0]==TokenType.WHILE or self.token[0]==TokenType.RETURN or self.token[0]==TokenType.IF or 
        self.token[0]==TokenType.PONTO_VIRGULA or self.token[0]==TokenType.NUM or self.token[0]==TokenType.PARENT_OP or 
        self.token[0]==TokenType.CHAVES_OP):
            self.statement()
            self.statement_list_()
    def local_declarations(self):
        if(self.token[0]==TokenType.INT or self.token[0]==TokenType.VOID):
            self.local_declarations_()
    def local_declarations_(self):
        if (self.token[0]==TokenType.INT or self.token[0]==TokenType.VOID):
            self.var_declaration()
            self.local_declarations_()
    def var_declaration(self):
        if (self.token[0]==TokenType.INT or self.token[0]==TokenType.VOID):
            self.type_specifier()
            self.match(TokenType.ID)
            self.var_declaration_()
        else:
            self.error()
    def type_specifier(self):
        if (self.token[0]==TokenType.INT or self.token[0]==TokenType.VOID):
            if(self.token[0]==TokenType.INT):
                self.match(TokenType.INT)
            elif(self.token[0]==TokenType.VOID):
                self.match(TokenType.VOID)
        else:
            self.error()   
    def var_declaration_(self):
        if (self.token[0]==TokenType.PONTO_VIRGULA or self.token[0]==TokenType.COLCH_OP):
            if (self.token[0]==TokenType.PONTO_VIRGULA):
                self.match(TokenType.PONTO_VIRGULA)
            elif(self.token[0]==TokenType.COLCH_OP):
                self.match(TokenType.COLCH_OP)
                self.match(TokenType.NUM)
                self.match(TokenType.COLCH_ED)
        else:
            self.error()
    def compound_stmt(self):
        if(self.token[0]==TokenType.CHAVES_OP):
            self.match(TokenType.CHAVES_OP)
            self.local_declarations()
            self.statement_list()
            self.match(TokenType.CHAVES_ED)
        else:
            self.error()
    def expression_stmt(self):
        if(self.token[0]==TokenType.PONTO_VIRGULA or self.token[0]==TokenType.NUM or self.token[0]==TokenType.PARENT_OP):
            if(self.token[0]==TokenType.PONTO_VIRGULA):
                self.match(TokenType.PONTO_VIRGULA)
            else:
                self.expression()
                self.match(TokenType.PONTO_VIRGULA)
        else:
            self.error()
    def statement(self):
        if(self.token[0]==TokenType.WHILE or self.token[0]==TokenType.RETURN or self.token[0]==TokenType.IF or 
        self.token[0]==TokenType.PONTO_VIRGULA or self.token[0]==TokenType.NUM or self.token[0]==TokenType.PARENT_OP or 
        self.token[0]==TokenType.CHAVES_OP):
            if(self.token[0]==TokenType.RETURN):
                self.return_stmt()
            elif(self.token[0]==TokenType.WHILE):
                self.iteration_stmt()
            elif(self.token[0]==TokenType.IF):
                self.selection_stmt()
            elif(self.token[0]==TokenType.CHAVES_OP):
                self.compound_stmt()
            else:
                self.expression_stmt()
        else:
            self.error()
    def factor(self):
        if(self.token[0]==TokenType.PARENT_OP):
            self.match(TokenType.PARENT_OP)
            self.additive_expression()
            self.match(TokenType.PARENT_ED)
        elif(self.token[0]==TokenType.NUM):
            self.match(TokenType.NUM)
        elif(self.token[0]==TokenType.ID):
            self.match(TokenType.ID)
            if(self.token[0]==TokenType.PARENT_OP):#call
                self.match(TokenType.PARENT_OP)
                self.args()
                self.match(TokenType.PARENT_ED)
            elif(self.token[0]==TokenType.COLCH_OP):#var
                self.match(TokenType.COLCH_OP)
                self.expression()
                self.match(TokenType.COLCH_ED)
        else:
            self.error()
    def args(self):
        if(self.token[0]==TokenType.ID or self.token[0]==TokenType.PARENT_OP or self.token[0]==TokenType.NUM):
            self.arg_list()
    def arg_list(self):
        if(self.token[0]==TokenType.ID or self.token[0]==TokenType.PARENT_OP or self.token[0]==TokenType.NUM):
            self.expression()
            self.arg_list_()
        else:
            self.error()
    def arg_list_(self):
        if(self.token[0]==TokenType.VIRGULA):
            self.match(TokenType.VIRGULA)
            self.expression()
            self.arg_list_()
        