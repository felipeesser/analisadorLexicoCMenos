import sys

from scanner import Scanner
from util import TokenType


def main():
    if len(sys.argv) == 2:
        scan = Scanner(sys.argv[1])
        token = scan.getToken()
        while token != TokenType.EOF:
            token = scan.getToken()
    else:
        print('Não foi passado arquivo de entrada')


if __name__ == '__main__':
    main()