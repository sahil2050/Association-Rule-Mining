#define a class transaction 
class Transaction:
    def __init__(self):
        self.items = set()
    
    def addItem(self,item):
        self.items.add(item)
    
    def contains(self,itemset):
        return itemset.issubset(self.items) 
    
    def allItems(self):
        return self.items
    
    def __str__(self):
        return str(self.items)
