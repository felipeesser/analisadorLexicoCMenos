from distutils.log import error
from tempfile import tempdir
from scanner import Scanner
from util import TokenType


class Parser:
    def __init__(self, filename):
        self.scanner = Scanner(filename)
        self.token=self.scanner.getToken()
    def error(self):
        print('erro')
        exit(1)
    def match(self,expectedToken):
        if (self.token[0]==expectedToken):
            self.token=self.scanner.getToken()
        else:
            self.error()
    def exp(self):
        temp=self.term()
        while(self.token[0]==TokenType.MAIS or self.token[0]==TokenType.MENOS):
            if(self.token[0]==TokenType.MAIS):
                self.match(TokenType.MAIS)
                temp+=self.term()
            elif(self.token[0]==TokenType.MENOS):
                self.match(TokenType.MENOS)
                temp-=self.term()
        return temp
    def term(self):
        temp=self.factor()
        while(self.token[0]==TokenType.MULT):
            self.match(TokenType.MULT)
            temp*=self.factor()
        return temp
    def factor(self):
        temp=None
        if(self.token[0]==TokenType.PARENT_OP):
            self.match(TokenType.PARENT_OP)
            temp=self.exp()
            self.match(TokenType.PARENT_ED)
        elif(self.token[0]==TokenType.NUM):
            temp=int(self.token[1])
            self.match(TokenType.NUM)
        else:
            self.error()
        return temp