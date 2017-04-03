import java.awt.Insets;
import java.lang.*;
import java.util.*;

public class Transaction {
    private Set<Integer> items;

    public Transaction(){
        items = new HashSet<Integer>();
    }
    public void addItem(Integer item){
        items.add(item);
    }

    public boolean contains(Integer item){
        return items.contains(item);
    }

    public boolean contains(Set<Integer> t){
        for(Integer x:t)
            if(!items.contains(x))
                return false;
        return true;
    }
    public Vector<Integer> itemsList(){
        Iterator<Integer> it = items.iterator();
        Vector<Integer> retVal = new Vector<Integer>();
        while(it.hasNext())
            retVal.add(it.next());
        return retVal;
    }

}