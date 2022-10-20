from grammar import grammar, production

def prueba_1():
    p1 = production("S", "aBDh")
    p2 = production("B", "cC")
    p3 = production("C", "_")
    p4 = production("C", "bC")
    p5 = production("D", "EF")
    p6 = production("E", "_")
    p7 = production("E", "g")
    p8 = production("F", "_")
    p9 = production("F", "f")
    G = grammar("G", ["a", "b", "c", "g", "f", "h"], ["S", "B", "C", "D", "E", "F"], [p1, p2, p3, p4, p5, p6, p7, p8, p9])
    G.calculate_table()
    print(G.first)
    print(G.follow)

def prueba_2():
    p1 = production("E", "TD")
    p2 = production("D", "+TD")
    p3 = production("D", "_")
    p4 = production("T", "FU")
    p5 = production("U", "*FU")
    p6 = production("U", "_")
    p7 = production("F", "(E)")
    p8 = production("F", "i")
    G = grammar("G", ["+", "*", "(", ")", "i"], ["E", "D", "T", "U", "F"], [p1, p2, p3, p4, p5, p6, p7, p8], "E")
    G.calculate_table()
    print(G.first)
    print(G.follow)

def prueba_3():
    p1 = production("S", "(L)")
    p2 = production("S", "a")
    p3 = production("L", "SM")
    p4 = production("M", ",SM")
    p5 = production("M", "_")
    G = grammar("G", ["a", ",", "(", ")"], ["S", "L", "M"], [p1, p2, p3, p4, p5])
    G.calculate_table()
    print(G.first)
    print(G.follow)

if __name__ == "__main__":
    prueba_1()
    prueba_2()
    prueba_3()
