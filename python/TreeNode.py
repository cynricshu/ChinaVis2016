class TreeNode(object):
    def __init__(self, name):
        self.name = name
        self.child = None


def tranverse(root, level):
    curr = root
    print("----" * level + curr.name)
    level += 1
    if curr.child is not None:
        for sonNode in curr.child:
            tranverse(sonNode, level)


def insert(root, father, name):
    if root.name == name:
        newNode = TreeNode(father)
        newNode.child = set()
        newNode.child.add(root)
        root = newNode
        return root
    else:
        return insertRecursive(root, father, name)


def insertRecursive(curr, father, name):
    if curr.name == father:
        if curr.child is None:
            curr.child = set()
        curr.child.add(TreeNode(name))
        return True
    else:
        if curr.child is not None:
            for sonNode in curr.child:
                return insertRecursive(sonNode, father, name)
        else:
            # print("no child anymore: " + curr.name)
            return False


def testTreeNode():
    root = TreeNode("1")

    res = insert(root, "1", "2")
    if type(res) is TreeNode:
        root = res

    insert(root, "2", "5")
    insert(root, "2", "6")
    insert(root, "2", "7")
    insert(root, "1", "3")
    insert(root, "1", "4")

    res = insert(root, "0", "1")
    if type(res) is TreeNode:
        root = res
    tranverse(root, 0)
