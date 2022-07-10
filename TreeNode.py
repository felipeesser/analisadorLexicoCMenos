class TreeNode:
    def __init__(self):
        self.children = []
        self.sibling = None
        self.lineno = None
        self.kind = None
        self.attr = None
        self.type = None

    def __str__(self):
        tree_string = ''
        i = 0
        tree = self
        while tree is not None:
            if tree.type == 'VAR-DECLARATION':
                tree_string += i * ' ' + 'Declaring variable: ' + tree.attr + '\n'
            elif tree.type == 'FUN-DECLARATION':
                tree_string += i * ' ' + 'Declaring function: ' + tree.attr + '\n'
            elif tree.type == 'PARAM':
                tree_string += i * ' ' + 'Param: ' + tree.attr + '\n'
            for child in tree.children:
                tree_string += ' ' + str(child)
            tree = tree.sibling
        return tree_string
