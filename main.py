import sys

from myparser import Parser
from scanner import Scanner
from util import printTree


def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        scanner = Scanner(filename)
        parse = Parser(scanner)
        tree = parse.parse()
        print('\nSyntax tree\n')
        print(printTree(tree, 0))
    else:
        print('Não foi passado arquivo de entrada')


if __name__ == '__main__':
    main()
