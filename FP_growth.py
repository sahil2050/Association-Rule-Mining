from transaction import *
#implement fp growth

data = set()
min_sup = 0
min_conf = 0

class Treenode:
    def __init__(self,value,support):
        self.value = value
        self.support = support
        self.parent = None
        self.children = set()
        self.linkage = None

    @property
    def value(self):
        return self.value

    @property
    def support(self):
        return self.support

    @property
    def parent(self):
        return self.parent

    @property
    def children(self):
        return self.children
    
    @property
    def linkage(self):
        return self.linkage

    def setParent(self,parent):
        self.parent = parent
    
    def inc_support(self,inc):
        self.support = self.support + inc

    def addChild(self,treenode):
        self.children.add(treenode)
    
    def getChildren(self):
        return self.children

    def isLeaf(self):
        return len(self.children) == 0
        
    def setLinkage(self,l):
        self.linkage = l
    
    def isRoot(self):
        return (self.value == None)


def insert_tree(treenode,l,link,currLink,support):
    if(len(l) == 0):
        return
    for child in treenode.getChildren():
        if(l[0] == child.value):
            child.inc_support(support)
            insert_tree(child,l[1:],link,currLink,support)
            return;
    node = Treenode(l[0],support)
    if l[0] in link and link[l[0]] == None:
        link[l[0]] = node
        #print "linking" + str(l[0])
    elif l[0] in link:
        #print "error "+str(l[0])
        currLink[l[0]].setLinkage(node)
    currLink[l[0]] = node
    #print "linkage set" + str(l[0])
    insert_tree(node,l[1:],link,currLink,support)
    node.setParent(treenode) 
    treenode.addChild(node)

def FP_tree(d,sup,conf):
    global data,min_sup,min_conf
    data = d
    min_sup = sup
    min_conf = conf
    support = {}
    link = {}
    currLink = {}
    for transaction in data:
        for x in transaction.allItems():
            support[x] = support.get(x, 0) + 1
    for key in support.keys():
        if (support[key] >= min_sup):
            link[key] = None
            currLink[key] = None
    #print support
    #print link
    #print sorted(support.keys(), key = support.get, reverse = True)
    tree = Treenode(None,None)
    for transaction in data:
        l = sorted(transaction.allItems(), key = support.get, reverse = True)
        l = [x for x in l if support[x] >= min_sup ]
        #print l
        insert_tree(tree,l,link,currLink,1)
        #for child in tree.getChildren():
        #    print (child.value,child.support)    
    return (tree,link,support)

def conditional_paths(tree,link,item):
    paths = []
    if not item in link:
        return paths
    node = link[item]
    while not node == None:
        path = []
        node_copy = node.parent
        while not node_copy.isRoot():
            #print path
            path.append(node_copy.value)
            node_copy = node_copy.parent
        if(len(path)>0):
            path.reverse()
            paths.append((path,node.support))
        #print "path" + str(path)
        node = node.linkage
    return paths

def conditional_fp_tree(paths):
    support = {}
    link = {}
    currLink = {}
    #print "$$" + str(paths)
    for (path,sup) in paths:
        for x in path:
            support[x] = support.get(x, 0) + sup
    for key in support.keys():
        if support[x] >= min_sup:
            link[x] = None
            currLink[x] = None
    #print support
    #print sorted(support.keys(), key = support.get, reverse = True)
    tree = Treenode(None,None)
    for (path,sup) in paths:
        l = [x for x in path if support[x] >= min_sup]
        insert_tree(tree,l,link,currLink,sup)
        #for child in tree.getChildren():
        #    print (child.value,child.support)    
    return (tree,link,support)

def is_single_path(tree):
    l =len(tree.getChildren())
    if(l==0):
        return True
    if(l > 1):
        return False
    x = True
    for child in tree.getChildren():
        x = is_single_path(child)
    return x

def get_path(tree):
    path = []
    while len(tree.getChildren())>0:
        for child in tree.getChildren():
            path.append(child.value)
            tree = child
            break
    return path

def get_all_combinations(path):
    if len(path) == 0:
        return [set()]
    allCombinations_1 = get_all_combinations(path[1:])
    allCombinations = []
    for c in allCombinations_1:
        allCombinations.append(c)
        _c = c.copy()
        _c.add(path[0])
        allCombinations.append(_c)
    return allCombinations

def FP_growth(tree,link,support,suffix):
    if is_single_path(tree):
        #generate all combinations
        #allCombinations = get_all_combinations(get_path(tree))
        #print allCombinations
        #for c in allCombinations:
        #    #print c
        #    for item in suffix:
        #        c.add(item)
        #print allCombinations
        path = get_path(tree)
        for item in suffix:
            path.append(item)
        return get_all_combinations(path) 
    else:
        frequent_itemsets = set()
        l = sorted(support.keys(), key = support.get, reverse = True)
        for item in l:
            (ctree,clink,csupport) = conditional_fp_tree(conditional_paths(tree,link,item))
            csuffix = suffix.copy()
            csuffix.add(item)
            for itemset in FP_growth(ctree,clink,csupport,csuffix):
                frequent_itemsets.add(frozenset(itemset))
        return frequent_itemsets

