import java.util.*;
import java.lang.*;
import java.io.*;


public class Apriori{
    private static Vector<Transaction> data; 
    private static int min_sup;

    public static Set<Set<Integer>> find_frequent_1_itemsets(){
        Map<Integer,Integer> map=new HashMap<Integer,Integer>(); // maps item id to support
        for(int i = 0; i < data.size(); i++){
            Transaction transaction = data.get(i);
            Vector<Integer> v = transaction.itemsList();
            for(int j = 0; j < v.size(); j++){
                if(map.containsKey(v.get(j))){
                    int support = map.get(v.get(j)) + 1;
                    map.remove(v.get(j));
                    map.put(v.get(j), support);
                }
                else{
                    map.put(v.get(j), 1);
                }
            }
        }   
        Set<Set<Integer>> l1 = new HashSet<Set<Integer>>(); 
        for (Map.Entry<Integer, Integer> entry : map.entrySet()) {
            Set<Integer> set = new HashSet<Integer>();
            if(min_sup <= entry.getValue()){
                set.add(entry.getKey());
                l1.add(set);
            }
            //System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
        }
        return l1;
    }

    public static boolean checkJoinCondition(Set<Integer> s1, Set<Integer> s2){
        if(s1.size() != s2.size())return false;
        int count_mismatches = 0;
        for(Integer x : s1)
            if(!s2.contains(x))count_mismatches++;
        return (count_mismatches == 1);
    }

    public static Set<Integer> setJoin(Set<Integer> s1, Set<Integer> s2){
        Set<Integer> retVal = new HashSet<Integer>();
        for(Integer x : s1)retVal.add(x);
        for(Integer x : s2)retVal.add(x);
        return retVal;
    }

    public static boolean has_infrequent_subset(Set<Integer> c,Set<Set<Integer>>  Lk_1){
        // cpy c to s
        Set<Integer> s = new HashSet<Integer>();
        for(Integer x : c) s.add(x);
        for(Integer x : c){
            s.remove(x);
            if(!Lk_1.contains(s))
                return true;
            s.add(x);
        }
        return false;
    }

    public static Set<Set<Integer>> apriori_gen(Set<Set<Integer>> Lk_1){
        Set<Set<Integer>> Ck = new HashSet<Set<Integer>>();
        Set<Integer> c;
        for(Set<Integer> l1 : Lk_1){
            for(Set<Integer> l2 : Lk_1){
                if(checkJoinCondition(l1,l2)){
                    c = setJoin(l1,l2);
                    if(!has_infrequent_subset(c,Lk_1))
                        Ck.add(c);
                }
            }
        }
        return Ck;
    }
    public static Set<Set<Integer>> frequentItemsets(){
        Set<Set<Integer>> retVal = new HashSet<Set<Integer>>();
        Set<Set<Integer>> l1 = find_frequent_1_itemsets();
        for(Set<Integer> s:l1)
            retVal.add(s);
        while(!l1.isEmpty()){
            Set<Set<Integer>> l = new HashSet<Set<Integer>>();
            Set<Set<Integer>> Ck = apriori_gen(l1);
            Map<Set<Integer>,Integer> map=new HashMap<Set<Integer>,Integer>();
            for(Transaction t: data){
                /*System.out.println("Transaction:");
                Vector<Integer> v = t.itemsList();
                for(int j=0; j<v.size(); j++)
                    System.out.printf("%d ", v.get(j));
                System.out.println("Ck size: "+Ck.size());*/
                for(Set<Integer> c: Ck){
                    if(t.contains(c)){
                        if(map.containsKey(c)){
                            
                            int support = map.get(c) + 1;
                            map.remove(c);
                            map.put(c, support);
                        }
                        else{
                            map.put(c, 1);
                        }
                    }
                }
            }
            for (Map.Entry<Set<Integer>, Integer> entry : map.entrySet()) {
                if(min_sup <= entry.getValue()){
                    /*Set<Integer> itemset = entry.getKey();
                    for(Integer x:itemset)
                        System.out.print(x + " ");
                    System.out.println("support :" + entry.getValue());*/
                    l.add(entry.getKey());
                    retVal.add(entry.getKey());
                }
            }
            l1 = l;
        }
        return retVal;
    }

    public static void main(String[] args) {
        data = new Vector<Transaction>();

        String inputFile = args[0];
        min_sup = Integer.parseInt(args[1]);

        BufferedReader br = null;
		FileReader fr = null;

		try {
			fr = new FileReader(inputFile);
			br = new BufferedReader(fr);
			String sCurrentLine;
			//br = new BufferedReader(new FileReader(FILENAME));
			while ((sCurrentLine = br.readLine()) != null) {
				//System.out.println(sCurrentLine);
                Transaction transaction = new Transaction();
                String[] strNums = sCurrentLine.split("\\s");
                for(int i = 0; i < strNums.length; i++ )
                    transaction.addItem(Integer.parseInt(strNums[i]));
                data.add(transaction);
			}
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (br != null)
					br.close();
				if (fr != null)
					fr.close();
			} catch (IOException ex) {
				ex.printStackTrace();
			}
        }
        
        Set<Set<Integer>>  itemsets = frequentItemsets();

        // Check if reading data works correctly
        /*System.out.println("Test");
        for(int i = 0; i < data.size(); i++){
            Transaction transaction = data.get(i);
            Vector<Integer> v = transaction.itemsList();
            for(int j=0; j<v.size(); j++)
                System.out.printf("%d ", v.get(j));
            System.out.println();
        }*/

        // printing frequent itemsets
        for(Set<Integer> itemset:itemsets){
            for(Integer x:itemset)
                System.out.print(x + " ");
            System.out.println();
        }
    }
}