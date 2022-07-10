class TreeNode:
    def __init__(self):
        self.children = []
        self.sibling = None
        self.attr = None
        self.type = None

    def __str__(self):
        return f'{self.type}'
