from nltk.corpus import wordnet
from collections import defaultdict
from os import system

words = wordnet.words()

setofwords = set(words)

partialsetofwords = set()
for word in setofwords:
    for i in range(1, len(word)):
        partialsetofwords.add(word[0:i])

board_len = 5

def check_word(word):
    return word in setofwords

def find_words(nodes):
    paths = []
    for n in nodes:
        dfs(n, paths=paths)
    words = list(set(paths))

    words.sort(reverse=True, key=lambda x: len(x))

    counts = defaultdict(list)
    for w in words:
        counts[len(w)].append(w)

    print("--------")

    # print the box
    for i in range(board_len):
        for j in range(board_len):
            end = ""
            if j == board_len - 1:
                end="\n"
            print(nodes[i*board_len+j].value, " ", end=end)
        
    print("--------")
    
    # print the words
    for k in counts:
        print(k, " : ", counts[k])

def dfs(node, paths, visited=[], path=""):
    path = path + node.value
    if len(path) >= 3: # min word size
        if check_word(path):
            paths.append(path)
    for neighbour in node.neighbours:
        if neighbour.loc not in visited and fuzzy_match(path):
            new_visited = [neighbour.loc, node.loc]
            new_visited.extend(visited)
            dfs(neighbour, paths, new_visited, path)

def fuzzy_match(partial_word):
    return partial_word in partialsetofwords

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

locs = [(i, j) for i in range(0, board_len) for j in range(0, board_len)]

flag = str(input('Use default board(b) or enter new one(n)? '))

board = ['e', 'f', 't', 'w', 'n', 't', 'i', 'e', 'r', 'b', 'w', 'qu', 's', 'g', 'y', 'f', 'e', 't', 'r', 'n', 'c', 'h', 'd', 'i', 'n']

print("Enter letters row wise starting from the top, going left to right.")
for i in range(board_len ** 2):
    letter = board[i] if flag == 'b' else str(input("enter letter: "))
    node = Node(letter, locs[i])
    nodes.append(node)

system('clear')

for n in nodes:
    for nei in nodes:
        if (n.loc[0] + 1 == nei.loc[0] and n.loc[1] == nei.loc[1]) or (n.loc[0] - 1 == nei.loc[0] and n.loc[1] == nei.loc[1]) or (n.loc[1] + 1 == nei.loc[1] and n.loc[0] == nei.loc[0]) or (n.loc[1] - 1 == nei.loc[1] and n.loc[0] == nei.loc[0]) or (n.loc[0] + 1 == nei.loc[0] and n.loc[1] + 1 == nei.loc[1]) or (n.loc[0] - 1 == nei.loc[0] and n.loc[1] - 1 == nei.loc[1]) or (n.loc[0] + 1 == nei.loc[0] and n.loc[1] - 1 == nei.loc[1]) or (n.loc[0] - 1 == nei.loc[0] and n.loc[1] + 1 == nei.loc[1]):
            n.add_neighbour(nei)
print('finding words...')
find_words(nodes)
