####################################################################
""" Podpunkt b) sprawozdania: FUNKCJE OPERUJĄCE NA ZBIORZE DANYCH"""

def unique_vals(data_set, attribute:str) -> set:
    """Znajduje unikalne wartości atrybutów w zbiorze trenującym."""
    return set(example[attribute] for example in data_set)

def class_val_count(data_set):
    """Oblicza liczbę wystąpień instancji danej klasy"""
    count = {'p': 0,
             'e': 0}
    for example in data_set:
        label = example['edibility']
        if label not in count:
            count[label] = 0
        count[label]+=1
    return count

import random
def predict_class_label(data_set):
    """Przewiduje etykietowanie danego zbioru na podstawie przykładów w nim zawartych
       Wybór jest realizowany metodą ruletkową, proporcjonalną do liczby instancji danej klasy"""
    
    class_count = class_val_count(data_set)
    e_label = class_count['e']
    p_label = class_count['p']
    
    p_label = p_label+e_label
    random_val = random.randint(0, p_label)
    
    if(random_val > 0 and random_val < e_label):
        return 'e'
    else:
        return 'p'


def partition(data_set, attribute:str):
    """Dzieli zbiór trenujący na podstawie testu atrybutu
    
       Wynikiem działania funkcji jest słownik, w którym jako klucze ustalone są unikalne wartości danego atrybutu
       w zbiorze data_set, natomiast jako wartości tych kluczy widnieją listy słowników, będące listami przykładów
       spełniających daną wartość atrybutu"""
    count = {}
    for example in data_set:
        label = example[attribute]
        if label not in count:
            count[label] = []
            count[label].append(example)
        else:      
            count[label].append(example)
    return count


####################################################################
""" Podpunkt c) sprawozdania: OPIS ELEMENTÓW DRZEWA"""

class Node:
    """Klasa reprezentujaca korzeń drzewa wybierający test dzielący zbiór trenujacy
       
       Atrybutami klasy są:
       Zbiór trenujący T będący zbiorem przykładów, na którym przeprowadzany jest test i podział
       Zapytanie test będące sprawdzanym w danym węźle atrybutem
       Lista węzłów (obiektów typu Node) children zawierające wyniki testu dla zbioru T w postaci węzłów/liści
       Wartość wyniku poprzedniego testu prev_test_val służąca prostemu wyróżnieniu na jakiej gałęzi jest węzeł
       
       Metoda predict() służy sprawdzeniu, czy dany przykład ze zbioru testujacego spełnia wynik testu dla którejś z
       gałęzi. W przypadku dojścia do liścia zwracane jest etykietowanie, w przypadku zatrzymania się w węźle,
       np. z powodu braku określonej wartości (gałęzi) dla danego przykładu testującego, zwracana jest 
       najpopularniejsza wartość etykietowania w danym węźle. Metoda find_code_pruning() zamienia wskazany w argumencie
       węzeł na liść, co jest wymagane w funkcji przycinania drzewa. Metoda get_nodes_list() zwraca listę węzłów danego    
       drzewa"""
    
    def __init__(self, T, prev_test_val):
        self.T = T
        self.test = ""
        self.children = []
        self.prev_test_val = prev_test_val
        self.node_list = []
        
    def predict(self, example) -> str:
        example_test_val = example[self.test]
        
        for child in self.children:
            if(child.prev_test_val == example_test_val):
                return(child.predict(example))

        return predict_class_label(self.T)
    
    
    def find_node_pruning(self, seeked_node):
        
        for i in range(0,len(self.children)):
            
            if self.children[i] is seeked_node:                
                self.children[i] = Leaf(self.children[i].T, self.children[i].prev_test_val)
            else:
                self.children[i].find_node_pruning(seeked_node)
                    
    
    
    def get_nodes_list(self):
        nodes_list = []
        
        for child in self.children:
            nodes_list_temp = child.get_nodes_list()
            for element in nodes_list_temp:
                if type(element) == Node:
                    nodes_list.append(element)
        nodes_list.append(self)
        return nodes_list
    
    @property
    def T(self):
        return self.__T
    
    @T.setter
    def T(self, T):
        self.__T = T

    @property
    def test(self):
        return self.__test
    
    @test.setter
    def test(self, test):
        self.__test = test
        
    @property
    def children(self):
        return self.__children
    
    @children.setter
    def children(self, children):
        self.__children = children
        
    @property
    def prev_test_val(self):
        return self.__prev_test_val
    
    @prev_test_val.setter
    def prev_test_val(self, prev_test_val):
        self.__prev_test_val = prev_test_val


class Leaf(Node):
    """Klasa reprezentujaca lisć budowanego drzewa, przypisującego etykietę do podzbioru przykładów.
    
    Zawiera etykietę jadalności grzyba (label) ustalaną na podstawie wyniku funkcji predict_clas_label na zbiorze
    T oraz atrybuty klasy Node, po której dziedziczy.
    
    Metoda predict() zwraca w klasie Leaf wartość etykietę w postaci wartości label danej instancji"""
    
    def __init__(self, T, prev_test_val):
        
        self.label = predict_class_label(T)
        super(Leaf, self).__init__(T, prev_test_val)
        
    def get_nodes_list(self):
        return []
    
    
    def find_node_pruning(self, seeked_node):
        pass
        
    def predict(self, example) -> str:
        return self.label
    
    @property
    def label(self):
        return self.__label
    
    @label.setter
    def label(self, label):
        self.__label = label

        
####################################################################
""" Podpunkt d) sprawozdania: OBLICZENIE JAKOŚCI TESTU"""
        

from math import log2
def entropy(T):
    """Oblicza i zwraca entropię zbioru uczącego T"""
    
    N = len(T)
    Ni_y = class_val_count(T)

    Ni = [Ni_y['p'], Ni_y['e']]
    
    if(Ni[0] == 0):
        E = -(Ni[1]/N)*log2(Ni[1]/N)
        
    elif(Ni[1] == 0):
        E = -(Ni[0]/N)*log2(Ni[0]/N)
    
    else:
        E = -(Ni[0]/N)*log2(Ni[0]/N)
        E += -(Ni[1]/N)*log2(Ni[1]/N)
    
    return E


def entropy_T(T, t:str):
    """Oblicza i zwraca entropię zbioru uczącego T ze względu na test t"""
    E_t = 0
    
    N = len(T)
    Ni_r = partition(T, t) 
    
    
    for attr_val in Ni_r:
        E_t += (len(Ni_r[attr_val])/N) * entropy(Ni_r[attr_val])
    
    return E_t


def info_gain(T, t):
    """Oblicza i zwraca zysk informacyjny zbioru uczącego T ze względu na test t"""
    
    return (entropy(T) - entropy_T(T,t))

        
####################################################################
""" Podpunkt e) sprawozdania: METODA RULETKOWA"""


import random
def roulette(T, S):
    """Funkcja wyboru testu metodą ruletkową
       T - zbiór trenujący
       S - zbiór możliwych testów 
       Każdy test ma szansę na bycie wybranym, bazując na wyniku jego zysku informacyjnego"""
    
    info_gain_results = {}
    prev_result = 0
    
    for test in S:
             
            info_gain_results[test] = info_gain(T, test) + prev_result  
            prev_result = info_gain_results[test]
     
    numb = random.uniform(0, prev_result)
    prev_result = 0
    
    for test_result in info_gain_results:
        
        if(numb > prev_result and numb < info_gain_results[test_result]):
            return test_result
        
        prev_result = info_gain_results[test_result]

def best_test(T,S):
    """Funkcja wyboru najlepszego możliwego testu dla porównania"""
    info_gain_results = 0
    best_result = 0 
    best_test = ''
    
    for test in S:
             
            info_gain_results = info_gain(T, test) 
            if info_gain_results > best_result:
                best_result = info_gain_results
                best_test = test
                
    return best_test
        
####################################################################
""" Podpunkt f) sprawozdania: ALGORYTM BUDOWY DRZEWA KLASYFIKACYJNEGO ID3"""


def ID3_build_tree(T, S, test_result, Z_min, L_min, mode) -> Node:
    """Algorytm ID3 budujący drzewo klasyfikacyjne
       T - zbiór trenujący
       S - zbiór możliwych testów
       test_result - wynik poprzedniego testu (gałęzi), wymagany w przypadku tworzenia kolejnych instancji węzłów/liści
       Z_min, L_min - parametry dot. budowy drzewa
       mode - decyduje o wyborze metody ruletkowej, bądź najlepszego testu
       
       Algorytm dokonuje kolejno sprawdzenia zawartości etykietowań każdej klasy w zbiorze T, aby ustalić, czy należy
       w miejsce obecnie tworzonego węzła wstawić lisć zgodny z najpospolitszym etykietowaniem. Sprawdzana też jest
       zawartość możliwych testów w zbiorze S. W przypadku braku decyzji o tworzeniu liścia następuje 'losowanie' 
       parametru dzielącego zbiór T i wyznaczanie kolejnych węzłów rekurencyjnie lub tworzenie liści w przypadku, gdy
       liczność podzbioru T__value jest mniejsza od określonej granicy.
       
       Jakość predykcji oraz wielkość drzewa uzależnione są od wartości parametrów Z_min oraz L_min.
       
       Wartością zwracaną przez algorytm jest węzeł/liść drzewa decyzyjnego
       Jako wynik algorytmu otrzymujemy drzewo klasyfykacyjne (a dokładniej jego korzeń) opisujące problem zadania"""
    
    main_node = Node(T, test_result)
    class_count = class_val_count(T)
    Z_edible = class_count['e']/len(T)
    Z_poisonous = class_count['p']/len(T)
    
    if(len(S) == 0 or (Z_edible >= Z_min and Z_poisonous >= Z_min)):
        return Leaf(T, test_result)
    elif(Z_edible >= Z_min):
        return Leaf(T, test_result)
    elif(Z_poisonous >= Z_min):
        return Leaf(T, test_result)
    else:
        if mode == True:
            A = roulette(T, S)
        else:
            A = best_test(T,S)
       
        main_node.test = A
        A_values = unique_vals(T, A)
        if '?' in A_values:
            A_values.remove('?')
        T_part = partition(T, A)
        S_part = S.copy()
        S_part.remove(A)
        children_nodes = []
        for value in A_values:
            T_value = T_part[value]

            if(len(T_value) <= L_min):
                children_nodes.append(Leaf(T_value, value))
                main_node.children = children_nodes
            else:
                children_nodes.append(ID3_build_tree(T_value, S_part, value, Z_min, L_min, mode))
                main_node.children = children_nodes
       
        
        return main_node
    
####################################################################
""" Podpunkt g) sprawozdania: FUNKCJE TESTUJĄCE DRZEWO"""

def test_tree(tree, test_set, printing):
    """Dokonuje predykcji w drzewie na podstawie zbioru testującego, wypisując liczbę sklasyfikowanych przykładów
       Wartość argumentu printing decyduje, czy wyniki zostaną wyświetlone na ekranie"""
    
    edible_labelled = 0
    
    for test in test_set:
        
        if(tree.predict(test) == 'e'):
            edible_labelled += 1
    
    poisonous_labelled = len(test_set) - edible_labelled
    
    real_labels = class_val_count(test_set)

    error = 100*(1 - abs(real_labels['e'] - edible_labelled)/len(test_set))
    if printing:
        print('Klasyfikacja drzewa:    e: %d  p: %d' % (edible_labelled, poisonous_labelled))
        print('Realne etykietowanie:   e: %d  p: %d' % (real_labels['e'], real_labels['p']))
        print('Poprawność etykietowania: %f' % error)
    return error


from math import floor
def cross_validation(X, S, iterations, printing, Z_min, L_min, mode):
    """Wykonuje walidację krzyżowa zbioru danych X
       Zbiór X dzielony jest na podzbior trenujący, testujący i zbiór służący do procedury przycinania
       Wartość argumentu printing decyduje, czy wyniki zostaną wyświetlone na ekranie 
       Wartością zwracaną przez funkcję jest lista otrzymanych jakości testowania dla każdej iteracji"""
    
    step = floor((len(X)-1000)/iterations)
    Train_set = []
    Test_set = []
    Pruning_set = []
    error_array = []
    nodes_array = []
    
    for i in range(iterations):
        
        
        Test_set = X[i*step:i*step+1000].copy()
        Pruning_set = X[7101:len(X)-1].copy()
        Train_set = X[0:7100].copy()
        
        for example in Test_set:
            Train_set.remove(example)   
        
        
        if printing:   
            print('\n')
            print("Drzewo dla iteracji nr.: %d" % (i+1))
            print("Zbiór testowy dla X[%d:%d]" % (i*step, i*step+1000))
            
        classification_tree = ID3_build_tree(Train_set, S, '', Z_min, L_min, mode)
        numb_nodes = len(classification_tree.get_nodes_list())
        classification_tree = tree_pruning(classification_tree, Pruning_set)
        numb_nodes = len(classification_tree.get_nodes_list())
        nodes_array.append(numb_nodes)
        error_array.append(test_tree(classification_tree, Test_set, printing))
    return error_array, nodes_array


####################################################################
""" Podpunkt h) sprawozdania: PRZYCINANIE DRZEWA"""

import copy
def tree_pruning(tree, data_set):
    """Przycina drzewo celem eliminacji nadmiarowych węzłów prowadzących do możliwego nadmiernego dopasowania
       do zbioru uczącego
       Argumentami funkcji są:
       tree- obiekt typu Node, korzeń główny budowanego drzewa
       data_set- niezależny zbiór o liczności 1000 przykładów, na którym przeprowadzana jest klasyfikacja
       
       Funkcja wyznacza jakość klasyfikacji dla podanego zbioru testowego, a następnie porównuje tę jakość
       dla przypadku, w którym któryś z węzłów jest zamieniony na lisć. Jeśli jakość ta jest wyższa, węzeł zostaje 
       zamieniony na liść, a nowym drzewem jest właśnie tak zmodyfikowana struktura.
       Wartością zwracaną jest więc korzeń drzewa, przyciętego lub nie w zależności od wyników"""
    
    
    quality = test_tree(tree, data_set, False)
    tree_temp = copy.deepcopy(tree)
    nodes_list = tree_temp.get_nodes_list()
    nodes_list_length = len(nodes_list)
    n = 0

    while(n < nodes_list_length):
    
        if(n < len(nodes_list)):
            node = nodes_list[n]
            
            tree_temp.find_node_pruning(node)
            quality_temp = test_tree(tree_temp, data_set, False)
            
            if quality_temp > quality: 
                quality = quality_temp
                tree = copy.deepcopy(tree_temp)
                tree_temp.get_nodes_list()
            else:

                tree_temp = copy.deepcopy(tree)       
                nodes_list = tree_temp.get_nodes_list().copy()

        n += 1
           
    return tree


