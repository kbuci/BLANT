import numpy as np

overcount = {1: 2, 2: 3, 4: 3, 3: 2, 6: 1, 5: 4, 7: 2, 8: 4, 11: 4, 10: 2, 14: 2, 9: 2, 12: 2, 16: 1, 17: 1, 13: 1, 19: 1, 23: 1, 20: 3, 22: 3, 18: 4, 15: 5, 21: 1, 24: 2, 25: 1, 26: 1, 27: 4, 28: 2, 29: 5, 0: 2}
cols_toExtract = [0, 1, 3, 4, 6, 8, 9, 12, 14, 15, 18, 22, 24, 27, 31, 34, 35, 39, 43, 45, 49, 51, 54, 56, 59, 62, 65, 68, 70, 72]

canon_list = None
upperToLower = None
K = 3

def set_upperToLower():
    global upperToLower, K
    upperToLower = np.loadtxt("orca_jesse_blant_table/UpperToLower"+str(K)+".txt", dtype='int')


def set_canon_list():
    global canon_list, K
    canon_list = np.loadtxt("canon_maps/canon_list"+str(K)+".txt", dtype='int', skiprows=1)

def lower_to_orca(lower):
    global upperToLower
    ordinals = upperToLower[:,4]
    rows = np.where(ordinals == lower)
        
    return upperToLower[rows[0], 7][0]

def lower_to_ord(lower):
    global upperToLower
    lowers = upperToLower[:,3]
    rows = np.where(lowers == lower)
        
    return upperToLower[rows[0], 4][0]

def ord_to_lower(ord):
    global upperToLower
    print(ord)
    ordinals = upperToLower[:,4]
    rows = np.where(ordinals == ord)
        
    return upperToLower[rows[0], 3][0]

def orca_to_lower(orca):
    global upperToLower
    orbits = upperToLower[:,7]
    rows = np.where(orbits == orca)    
    return upperToLower[rows[0], 4][0]

def edgesFromFile(lower):
    global canon_list
    ordinals = canon_list[:,0]
   
    rows = np.where(ordinals == lower)

    return canon_list[rows[0],2][0]

class Graphlet:
    def __init__(self,**kwargs):
        global K
        self.orca = kwargs['orca'] if 'orca' in kwargs else None
        self.lower_ord = kwargs['lower_ord'] if 'lower_ord' in kwargs else None
        if self.lower_ord:
            self.lower_decimal = ord_to_lower(self.lower_ord)
        if self.orca == None and K <= 5:
            self.orca = lower_to_orca(self.lower_ord)
        elif self.lower_decimal == None and K <= 5:
            self.lower_decimal = orca_to_lower(self.orca)
        self.lower_ord = lower_to_ord(self.lower_decimal)

        assert self.lower_decimal != None

        self.edges = kwargs['edges'] if 'edges' in kwargs else edgesFromFile(self.lower_decimal)

    def isTree(self):
        global K
        return self.edges == K - 1

    def isClique(self):
        global K
        return self.edges == K * (K-1) // 2

    def isStar(self):
        global K
        if self.edges != K - 1:
            return False
        global canon_list
        edges = canon_list[:,2]
        rows = np.where(edges == K - 1)
        return canon_list[rows[0],0][0] == self.lower_ord

if __name__ == "__main__":
    global K
    K = 5
    set_canon_list()
    set_upperToLower()
    for o in range(9,30):
        g = Graphlet(orca=o)
        print(o, g.lower_decimal, g.isTree(), g.isStar(), g.isClique())
