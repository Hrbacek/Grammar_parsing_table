import numpy as np
import pandas as pd
import itertools

from get_grammar import input

class production:
    def __init__(self, head:str, body:str):
        self.head = head
        self.body = body
    
    def __str__(self) -> str:
        return f"{self.head} --> {self.body}"
    
    def __repr__(self) -> str:
        return f"production(\"{self.head}\",\"{self.body}\")"
    
class grammar:
    def __init__(self, id:str, terminals:list, nonterminals:list, productions:list, start_var="S"):
        self.id = id
        self.terminals = terminals
        self.nonterminals = nonterminals
        
        endmarker = ["$"]
        self.terminals_endmarker = terminals+endmarker
        
        self.productions = productions
        self.start_var = start_var
        self.first = {nonterminal:set() for nonterminal in self.nonterminals}
        self.follow = {nonterminal:set() for nonterminal in self.nonterminals}
        
        self.parsing_table = np.empty((len(self.nonterminals), len(self.terminals)+1), dtype=object)
        for i,j in itertools.product(range(len(self.nonterminals)), range(len(self.terminals_endmarker))):
            self.parsing_table[i,j] = set()
        self.parsing_table = pd.DataFrame(self.parsing_table, index=self.nonterminals, columns=self.terminals_endmarker, dtype=object)
    
    def __str__(self) -> str:
        output = f"\nGrammar {self.id}:\n"
        for production in self.productions:
            output += f"{str(production)}\n"
        return output  
    
    def get_firsts(self):
        for production in self.productions:
            if production.body == "_":
                self.first[production.head].add("_")
        for _ in self.nonterminals:
            for production in self.productions:
                    if production.body != "_":
                        position=0
                        flag = True
                        while flag and position<=(len(production.body)-1):
                            if production.body[position] in self.terminals:
                                self.first[production.head].add(production.body[position])
                                if position==0:
                                    flag = False
                            else:        
                                aux = self.first[production.body[position]].copy()
                                aux.discard("_")
                                self.first[production.head] = self.first[production.head].union(aux)
                            if production.body[position] in self.nonterminals:
                                if "_" not in self.first[production.body[position]]:
                                    flag = False
                            position += 1
                        if flag == True and position!=1 :
                            self.first[production.head].add("_")
    
    def apply_first(self, string:str)-> set:
        first_string = set()
        for position in range(len(string)-1,-1,-1):
            flag = 1
            for i in range(0,position):
                if string[i] in self.terminals:
                    in_lambda = 0
                else:
                    in_lambda = "_" in self.first[string[i]]
                flag = flag*in_lambda
            if flag:
                if string[position] in self.terminals:
                    first_string.add(string[position])
                else:
                    if string[position] == "_":
                        first_string.add("_")
                    else:
                        aux = self.first[string[position]].copy()
                        if position == len(string)-1 and "_" in self.first[string[position]]:
                            first_string = first_string.union(aux)
                        else:
                            aux.discard("_")
                            first_string = first_string.union(aux)
        return first_string
                
    def get_follow(self):
        self.follow[self.start_var].add("$")
        for _ in self.nonterminals:
            for production in self.productions:
                    string = production.body
                    for position in range(len(production.body)):
                        if string[position] in self.nonterminals:
                            beta = string[position+1:]
                            if beta != "":
                                if "_" in self.apply_first(beta):
                                    follow_head = self.follow[production.head]
                                    self.follow[string[position]] = self.follow[string[position]].union(follow_head)
                                first_beta = self.apply_first(beta)
                                first_beta.discard("_")
                                self.follow[string[position]] = self.follow[string[position]].union(first_beta)
                            else:
                                follow_head = self.follow[production.head]
                                self.follow[string[position]] = self.follow[string[position]].union(follow_head)
                    
    def get_parsing_table(self):
        for production in self.productions:
            first_alpha = self.apply_first(production.body)
            for simbol in first_alpha:
                if simbol != "_":
                    self.parsing_table.loc[production.head,simbol].add(production)
                    pass
            if "_" in first_alpha:
                follow_head = self.follow[production.head]
                for simbol in follow_head:
                    if simbol != "_":
                        self.parsing_table.loc[production.head,simbol].add(production)
                if "$" in follow_head:
                    self.parsing_table.loc[production.head,"$"].add(production)
    
    def calculate_table(self):
        self.get_firsts()
        self.get_follow()
        self.get_parsing_table()
        print(self)
        print(self.parsing_table)
                    
def main():
    name, terminals, nonterminals, prods, initial = input[0][0], input[1], input[2], input[3], input[4][0] 
    prods = [production(head, body) for (head,body) in prods]
    G = grammar(name, terminals, nonterminals, prods, initial)
    G.calculate_table()
    print("FIRST",G.first,sep="\n")
    print("FOLLOW",G.follow,sep="\n")

if __name__ == "__main__":
    main()

