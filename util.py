from enum import Enum

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']
RESERVED_WORDS = ['else', 'if', 'int', 'return', 'void', 'while']


class TokenType(Enum):
    ID = 1
    NUM = 2
    PLUS = 3
    MINUS = 4


class StateType(Enum):
    START = 1
    DONE = 2
    INID = 3
    INMULT = 4
    INDIV = 5
    INNUM = 6
    MAYBE_COMMENT = 7
    COMMENT = 8
    INCOMMENT = 9
    OTHER = 10


def readFile(fileName):
    try:
        file = open(fileName, 'r')
        program = file.read().splitlines()
        file.close()
        return program
    except FileNotFoundError:
        raise FileNotFoundError('Arquivo não encontrado')


def isDigit(c):
    if c in DIGITS:
        return True
    return False


def isLetter(c):
    if c in LETTERS:
        return True
    return False


def reservedLookup(tokenString):
    for palavraChave in RESERVED_WORDS:
        if tokenString == palavraChave:
            return 'Palavra-Chave'
    return 'ID'


def printToken(tokenType, tokenString):
    pass
