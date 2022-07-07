import sys

from scanner import Scanner
from util import TokenType
from parser import Parser

def main():
    if len(sys.argv) == 2:
        # scan = Scanner(sys.argv[1])
        # token = scan.getToken()
        # while token != TokenType.EOF:
        #     token = scan.getToken()
        parse=Parser(sys.argv[1])
        print(parse.exp())
    else:
        print('Não foi passado arquivo de entrada')


if __name__ == '__main__':
    main()
