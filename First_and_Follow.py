# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 17:33:03 2019

@author: Lenovo
"""
import argparse

def first_single_symbol(rules,terminals):
    first={}
    for t in terminals:
       first[t]=set([t]) 
    for k in rules:
       first[k]=set() 
    change=True
    while(change):
        change=False
        for nonter,lhs in rules.items():
            for i in lhs:
                l=first[i[0]]
                for j in i:
                  l=l .intersection (first[j] )  
                if "epsilon" in l:
                    if "epsilon" not in first[nonter]:
                              first[nonter]=first[nonter].union(set(["epsilon"]))
                              change=True
                else:
                    for indx in range(0,len(i)):
                        l=first[i[0]]
                        b=i[:indx]

                        for val in b: 
                                l=l.intersection(first[val])
                        if indx==0 or  "epsilon" in l:
                                s1=first[i[indx]] - set(["epsilon"])
                                if not (bool(s1) and s1 <= (first[nonter])):  
                                    first[nonter]=first[nonter].union(first[i[indx]]-set(["epsilon"]))
                                    change=True  

    #print(first)
    return first

def find_first(first,rules,terminals):
    for lhs,rhs in rules.items():
        for li in rhs:
            if len(li)>1:
                s=first[li[0]]
                i=1
                while("epsilon"  in s and i<len(li)):
                    s=s-set(["epsilon"])
                    s=s.union(first[li[i]])
                    i=i+1
                first[lhs]= first[lhs].union(s)
    
    #print(first)
    return first
"""
{'S': [['S', 'A', 'B'], ['S', 'B', 'C'], ['epsilon']], 
'A': [['a', 'A', 'a'], ['epsilon']], 
'B': [['b', 'B'], ['epsilon']], 
'C': [['c', 'C'], ['epsilon']]}
"""      
def find_follow(rules,first,start,terminals):
    follow={}
    non_terminals=[]
    for k in rules:
       follow[k]=set() 
       non_terminals.append(k)
    follow[start]=set("$")   
    change=True
    while(change):
        change=False
        for lhs,rhs in rules.items():
            for li in rhs:
                for nonterminal in (non_terminals):
                    if nonterminal in li:
                        indx=li.index(nonterminal)
                        if indx<len(li)-1:
                           direct_first=first[li[indx+1]]
                           first_so_far=direct_first
                           for i in range(indx+1,len(li)):
                             direct_first=first[li[i]]  
                             first_so_far=first_so_far.intersection(first[li[i]])
                             if not ((direct_first-set(["epsilon"])).issubset( follow[nonterminal])):
                                 follow[nonterminal]=follow[nonterminal].union(direct_first-set(["epsilon"]))
                                 change=True
                             if not (li[i] in non_terminals and "epsilon" in first_so_far) :
                                 break
                           if "epsilon" in first_so_far:
                              if not (follow[lhs].issubset(follow[nonterminal])):
                                     follow[nonterminal]=follow[nonterminal].union(follow[lhs])
                                     change=True 
                        else:
                            if not (follow[lhs].issubset(follow[nonterminal])):
                                     follow[nonterminal]=follow[nonterminal].union(follow[lhs])
                                     change=True                                
    #print(follow)
    return follow
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')
    
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                            metavar="file")
    
    args = parser.parse_args()
    rules={}
    with open(args.file, mode='r', encoding='utf-8-sig') as file:
        first_line = file.readline()
        start=first_line[0]
    with open(args.file, mode='r', encoding='utf-8-sig') as file:
        for line in file:
            x=line.split(':')
            y=x[1:]
            z=y[0].split('|')
            l=[]
            for i in z:
                p=i.strip('\n')
                j=[p]
                l.append(j)
            kk=x[0].strip(' ')  
            rules[kk]=l
    for k, v in rules.items():
                li=[]
                for o in v:
                    l=[]
                    if o[0] !=" epsilon":
                        j=o[0].split(' ')
                        #print(j)
                        
                        for jj in j:
                            if jj!='':
                                l.append(jj)
                        li.append(l)
                    else: 
                       str1= o[0].strip(' ')
                       li.append([str1])
                rules[k]=li

    terminals=[]
    for k,v in rules.items():
      for i in v:  
         if i=='epsilon':
            if i not in terminals:
               terminals.append(i)
         else:    
            for ii in i:
                if ii not in terminals and ii not in rules.keys():
                    terminals.append(ii)      
    #print(rules)
    first=first_single_symbol(rules,terminals)
    find_first(first,rules,terminals)
    follow=find_follow(rules,first,start,terminals)
    output_file=open(args.file[:-4]+"__Output.txt","w+") 

    for key in rules.keys():
        f=first[key]
        fo=follow[key]
        str1 = ' '.join(f)
        str2=' '.join(fo)
        output_file.write(key+' '+":"+' '+str1+" "+":"+" "+str2)
        output_file.write("\n")
    output_file.close()
