from lib2to3.pgen2 import token


class Scanner():
    ESTADOS={'start':False,'end':False,'other':False,'inid':False,'incomment':False}

    PCHAVES=['else','if','int','return','void','while']

    LETRA=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    DIGITO=['0','1','2','3','4','5','6','7','8','9']

    OPERADORES={
        '+': '',
        '-': '',
        '*': '',
        '/': '',
        '<': '',
        '<=' : '',
        '>': '',
        '>=' : '',
        '==' : '',
        '!=' : '',
        '=': '',
        ';': '',
        ',': '',
        '(': '',
        ')': '',
        '[': '',
        ']': '',
        '{': '',        
        '}': '',
        '/*': '', 
        '*/': ''
    }
    
    def __init__(self):
        self.tokens = []
        self.setEstado('start')

    def setEstado(self,estado):
        for e in self.ESTADOS:
            self.ESTADOS[e]=False
        self.ESTADOS[estado]=True

    def getEstado(self,estado):
        return self.ESTADOS[estado]

    def vLetra(self,c):
        if c in self.LETRA:
            return True
        return False

    def vPalavra(self,token):
        for c in token:
            if c not in self.LETRA:
                return False
        return True

    def vChave(self,token):
        if token not in self.PCHAVES:
            return False
        return True         

    def classifica(self,token,index):
        if self.vPalavra(token):
            if self.vChave(token):
                self.tokens.append([index,'Palavra-Chave',token])
            else:
                self.tokens.append([index,'ID',token])

    def leitura(self,nomeArq):
        file=open(nomeArq,'r')
        programa=file.read().splitlines()
        file.close()
        return programa

    def scan(self,nomeArq):
        try:
            programa=self.leitura(nomeArq)
            for linha in programa:
                index=str(programa.index(linha))
                token=''
                for c in linha:
                    if self.getEstado('start'):
                        if self.vLetra(c):
                            self.setEstado('inid')

                    elif self.getEstado('inid'):
                        if self.vLetra(c):
                            self.setEstado('inid')
                        elif c==' ':
                            c=''
                            self.setEstado('end')
                        else:
                            self.setEstado('other')

                    if not self.getEstado('other'):       
                        token+=c

                    if self.getEstado('end') or self.getEstado('other'):
                        self.classifica(token,index)
                        if self.getEstado('other'):
                            pass    
                        token=''
                        self.setEstado('start')
                #quebra de linha
                if token:
                    self.classifica(token,index)
                    if self.getEstado('other'):
                        pass    
        except FileNotFoundError:
            raise FileNotFoundError('arquivo não encontrado')

    def saida(self):
        for t in self.tokens:
            print(t[0]+': '+t[1]+', '+t[2])

