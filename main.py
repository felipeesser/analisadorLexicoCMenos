import sys

from myparser import Parser
from scanner import Scanner


def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        scanner = Scanner(filename)
        parse = Parser(scanner)
        tree = parse.parse()
        print('\nSyntax tree\n')
        print(tree)
    else:
        print('Não foi passado arquivo de entrada')


if __name__ == '__main__':
    main()
