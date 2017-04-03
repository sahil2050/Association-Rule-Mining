import sys
from transaction import *

data = set()
min_sup = 0
min_conf = 0

#implememnt apriori
def find_frequent_1_itemsets():
    support = {}
    for transaction in data:
        for x in transaction.allItems():
            support[x] = support.get(x, 0) + 1
    #print support
    return set(frozenset({item}) for item in support if support[item] >= min_sup)

def check_join_condition(l1,l2):
    if(len(l1) != len(l2)):
        return False
    return (len(l1-l2)==1)

def has_infrequent_subset(c,Lk_1):
    s = set()
    for item in c:
        s.add(item)
    for item in c:
        s.remove(item)
        if not s in Lk_1:
            return True
        s.add(item)
    return False

def apriori_gen(Lk_1):
    Ck = set()
    for l1 in Lk_1:
        for l2 in Lk_1:
            if check_join_condition(l1,l2):
                c = l1 | l2
                if not has_infrequent_subset(c,Lk_1):
                    Ck.add(c)
    return Ck

def apriori_frequent_itemsets(d,sup,conf):
    global data,min_sup,min_conf
    data = d
    min_sup = sup
    min_conf = conf
    l1 = find_frequent_1_itemsets()
    retValue = l1.copy()
    while(len(l1)!=0):
        l = set()
        Ck = apriori_gen(l1)
        #print Ck
        support = {}
        for transaction in data:
            for c in Ck:
                if(transaction.contains(c)):
                    support[c] = support.get(c,0) + 1
        #print support
        for itemset in support:
            if (support[itemset] >= min_sup):
                l.add(itemset)
                retValue.add(itemset)
        l1 = l
    return retValue
