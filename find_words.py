from nltk.corpus import wordnet
from collections import defaultdict
from os import system
from tqdm import tqdm

setofwords = set(wordnet.words())

def check_word(word):
    return word in setofwords

def find_words(nodes):
    paths = []
    for n in nodes:
        dfs(n, paths=paths)
        print('finding words...', end="\r")
    words = [w for w in set(paths) if check_word(w)]

    words.sort(reverse=True, key=lambda x: len(x))

    counts = defaultdict(list)
    for w in words:
        counts[len(w)].append(w)

    print("--------")

    # print the box
    for i in range(4):
        for j in range(4):
            end = ""
            if j == 3:
                end="\n"
            print(nodes[i*4+j].value, " ", end=end)
        
    print("--------")
    
    # print the words
    for k in counts:
        print(k, " : ", counts[k])

def dfs(node, paths, visited=[], path=""):
    path = path + node.value
    if len(path) >= 3:
        paths.append(path)
    for neighbour in node.neighbours:
        if neighbour.loc not in visited:
            new_visited = [neighbour.loc, node.loc]
            new_visited.extend(visited)
            dfs(neighbour, paths, new_visited, path)

class Node:

    def __init__(self, value, loc):
        self.loc = loc
        self.value = value
        self.neighbours = []

    def add_neighbour(self, node):
        self.neighbours.append(node)

    def add_neighbours(self, nodes):
        self.neighbours.extend(nodes)

    def __repr__(self):
        nei_names = [n.value for n in self.neighbours]
        return "loc: {}, value: {}, neighbours: {}".format(self.loc, self.value, nei_names)

nodes = []

locs = [(i, j) for i in range(0, 4) for j in range(0, 4)]

print("Enter letters row wise starting from the top, going left to right.")
for i in range(16):
    letter = str(input("enter letter: "))
    node = Node(letter, locs[i])
    nodes.append(node)

system('clear')

for n in nodes:
    for nei in nodes:
        if (n.loc[0] + 1 == nei.loc[0] and n.loc[1] == nei.loc[1]) or (n.loc[0] - 1 == nei.loc[0] and n.loc[1] == nei.loc[1]) or (n.loc[1] + 1 == nei.loc[1] and n.loc[0] == nei.loc[0]) or (n.loc[1] - 1 == nei.loc[1] and n.loc[0] == nei.loc[0]) or (n.loc[0] + 1 == nei.loc[0] and n.loc[1] + 1 == nei.loc[1]) or (n.loc[0] - 1 == nei.loc[0] and n.loc[1] - 1 == nei.loc[1]) or (n.loc[0] + 1 == nei.loc[0] and n.loc[1] - 1 == nei.loc[1]) or (n.loc[0] - 1 == nei.loc[0] and n.loc[1] + 1 == nei.loc[1]):
            n.add_neighbour(nei)

find_words(nodes)
