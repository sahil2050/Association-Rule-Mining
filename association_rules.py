import sys
from transaction import *
from apriori import *
from FP_growth import *

data = set()
min_sup = 0
min_conf = 0


def get_support(s):
    ans = 0
    for transaction in data:
        if transaction.contains(s):
            ans = ans + 1
    return float(ans)

#generates all association rules for a set s
def association_rules(s):
    rules = []
    subsets = get_all_combinations(list(s))
    for subset in subsets:# subset => s - subset
        if(len(subset) > 0 and len(subset) < len(s)):
            support = get_support(s)
            confidence = support/get_support(subset)
            #print confidence
            if(confidence >= min_conf):
                rules.append(str(subset) + "=>" + str(s-subset)+ " support: " + str(support/len(data)) + " confidence: " + str(confidence))
    return rules


def main():
    filename = sys.argv[1]
    #read transactions from input file
    with open(filename, 'r') as fobj:
        for line in fobj:
            t = Transaction()
            for num in line.split():
                t.addItem(int(num))
            data.add(t)
    global min_sup,min_conf
    min_sup = float(sys.argv[2])*len(data)
    min_conf = float(sys.argv[3])



    fp_tree,link,support = FP_tree(data,min_sup,min_conf)
    #print min_sup
    #print link[3].value
    #item = 5
    #paths = conditional_paths(fp_tree,link,item)
    #print "paths" + str(paths)
    #l = [1,2,3]
    #print get_all_combinations(l)
    #l = [39,48,38,32,41,65]
    #for i in l:
    #    print conditional_paths(fp_tree,link,i)
    #fp_tree,link,support = conditional_fp_tree(conditional_paths(fp_tree,link,32))
    #print support
    #print link
    #for child in fp_tree.getChildren():
    #    print str(child.value) + ' '+ str(child.support)
    #    print "##"
    #    for c in child.getChildren():
    #          print str(c.value) + ' '+ str(c.support)
    #print "$$"
    #print conditional_paths(fp_tree,link,48)
    #fp_tree,link,support = conditional_fp_tree(conditional_paths(fp_tree,link,48))
    #print support
    #for child in fp_tree.getChildren():
    #    print str(child.value) + ' '+ str(child.support)
    #    print "##"
    #    for c in child.getChildren():
    #          print str(c.value) + ' '+ str(c.support)
    #print "$$"
    #print get_support(set([32,39,48]))
    rules = []
    print ("------------------------")
    print ("min_sup " + sys.argv[2])
    print ("min_conf " + str(min_conf))
    print ("------------------------")
    print "frequent itemsets"
    if sys.argv[4] == "fp":
        for itemset in FP_growth(fp_tree,link,support,set()):
            rules = rules + association_rules(itemset)
            for item in itemset:
                sys.stdout.write(str(item)+' ')
            if (len(itemset) > 0):
                sys.stdout.write('\n')
    elif sys.argv[4] == "apriori":
        for itemset in apriori_frequent_itemsets(data,min_sup,min_conf):
            rules = rules + association_rules(itemset)
            for item in itemset:
                sys.stdout.write(str(item)+' ')
            if (len(itemset) > 0):
                sys.stdout.write('\n')
    print ("------------------------")
    print "association rules"
    for rule in rules:
        print rule
    

if __name__ == "__main__":
    main()
