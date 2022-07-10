from enum import Enum


# Enum para os tipos de token


class TokenType(Enum):
    ID = 1
    NUM = 2
    ATTR = 3
    MAIS = 4
    MENOS = 5
    MULT = 6
    DIV = 7
    DIF = 8
    EQUAL = 9
    GREAT = 10
    GREAT_EQUAL = 11
    LESS = 12
    LESS_EQUAL = 13
    COLCH_OP = 14
    COLCH_ED = 15
    PARENT_OP = 16
    PARENT_ED = 17
    CHAVES_OP = 18
    CHAVES_ED = 19
    PONTO_VIRGULA = 20
    VIRGULA = 21
    EOF = 23
    IF = 24
    ELSE = 25
    INT = 26
    RETURN = 27
    VOID = 28
    WHILE = 29
    ERROR = 30


# Enum para os tipos de estado do scanner
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
    MAYBE_GREATER = 10
    MAYBE_LESS = 11
    MAYBE_EQ = 12
    DIFF = 13


DIGITOS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LETRAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
          'v', 'w', 'x', 'y', 'z',
          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
          'V', 'W', 'X', 'Y', 'Z']
PALAVRAS_RESERVADAS = {'if': TokenType.IF, 'else': TokenType.ELSE, 'int': TokenType.INT, 'return': TokenType.RETURN,
                       'void': TokenType.VOID, 'while': TokenType.WHILE}


def readFile(fileName):
    try:
        file = open(fileName, 'r')
        program = file.read().splitlines()
        file.close()
        return program
    except FileNotFoundError:
        raise FileNotFoundError('Arquivo não encontrado')


def isDigit(c): return c in DIGITOS


def isLetter(c): return c in LETRAS


def reservedLookup(tokenString):
    try:
        return PALAVRAS_RESERVADAS[tokenString]
    except:
        return TokenType.ID


def printToken(tokenType, tokenString, lineno):
    if tokenType in PALAVRAS_RESERVADAS.values():
        print('    ' + str(lineno) + ': PALAVRA RESERVADA, ' + tokenString)
    elif tokenType == TokenType.ID:
        print('    ' + str(lineno) + ': ' + tokenType.name + ', name = ' + tokenString)
    elif tokenType == TokenType.NUM:
        print('    ' + str(lineno) + ': ' + tokenType.name + ', value = ' + tokenString)
    elif tokenType == TokenType.EOF:
        print(str(lineno) + ': ' + tokenType.name)
    else:
        print('    ' + str(lineno) + ': ' + tokenType.name + ', ' + tokenString)


def printTree(tree, i):
    tree_string = ''
    while tree is not None:
        tree_string += i * '  '
        if tree.type == 'VAR-DECLARATION':
            tree_string += 'Declaring variable:\n'
        elif tree.type == 'FUN-DECLARATION':
            tree_string += 'Declaring function:\n'
        elif tree.type == 'TYPE-SPECIFIER':
            tree_string += f'Type: {tree.attr}\n'
        elif tree.type == 'ID':
            tree_string += f'ID: {tree.attr}\n'
        elif tree.type == 'PARAMS':
            tree_string += 'Params:\n'
        elif tree.type == 'PARAM':
            tree_string += 'Param:\n'
        elif tree.type == 'COMPOUND-STMT':
            tree_string += 'Compound statement:\n'
        elif tree.type == 'SELECTION-STMT':
            tree_string += 'If:\n'
        elif tree.type == 'ITERATION-STMT':
            tree_string += 'While:\n'
        elif tree.type == 'RETURN-STMT':
            tree_string += 'Return:\n'
        elif tree.type == 'EXPRESSION-STMT':
            tree_string += 'Expression statement:\n'
        elif tree.type == 'ASSIGN':
            tree_string += f'Assign to: {tree.attr}\n'
        elif tree.type == 'SIMPLE-EXPRESSION':
            tree_string += 'Simple expression:\n'
        elif tree.type == 'EXPRESSION':
            tree_string += 'Expression:\n'
        elif tree.type == 'RELOP' or tree.type == 'ADDOP' or tree.type == 'MULOP':
            tree_string += f'Op: {tree.attr}\n'
        elif tree.type == 'ADDITIVE-EXPRESSION':
            tree_string += 'Additive expression:\n'
        elif tree.type == 'TERM':
            tree_string += 'Term:\n'
        elif tree.type == 'FACTOR':
            tree_string += 'Factor:\n'
        elif tree.type == 'NUM':
            tree_string += f'Const: {tree.attr}\n'
        elif tree.type == 'CALL':
            tree_string += f'Call: {tree.attr}\n'
        elif tree.type == 'VAR':
            tree_string += f'Var: {tree.attr}\n'
        i += 1
        for child in tree.children:
            tree_string += printTree(child, i)
        tree = tree.sibling
        i -= 1
    return tree_string
