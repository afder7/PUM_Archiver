import sys
from collections import Counter
import json
from itertools import cycle
dictionary = dict()


def traverse(tree):
    if not tree.left:
        return
    tree.left.root = tree.root + "0"
    tree.right.root = tree.root + "1"
    # print(tree.left.root, tree.right.root)
    traverse(tree.left)
    traverse(tree.right)


def temp_dfs(tree):
    if tree.value:
        dictionary[tree.value] = tree.root
        return
    temp_dfs(tree.left)
    temp_dfs(tree.right)


class Tree:
    # if right and left are missing input value

    def __init__(self, value=None, left=None, right=None):
        self.root = ""
        self.value = value
        self.left = left
        self.right = right
        if left:
            self.left.root += "0"
            traverse(self.left)
        if right:
            self.right.root += "1"
            traverse(self.right)

    def change_left(self, new_val):
        self.left = new_val

    def change_right(self, new_val):
        self.right = new_val

    def change_value(self, new_val):
        self.value = new_val

    def __repr__(self):
        return f"root - {self.root};" \
               f"left - {self.left};" \
               f"right - {self.right};" \
               f"value - {self.value}"


def vigineree(text, du, keytext):
    viginere = sorted(list(du.keys()))
    # print(viginere)
    return "".join(map(lambda x: viginere[(viginere.index(x[0]) + ord(x[1])) % len(viginere)], zip(text, cycle(keytext))))


def encode(keyword=None):

    def key_giver(d):
        if len(d) <= 1:
            return d
        least_met_elems = sorted(list(d.items()), key=lambda x: x[1])[:2]
        # print(least_met_elems)
        a = d.pop(least_met_elems[0][0])
        b = d.pop(least_met_elems[1][0])
        d[Tree(left=least_met_elems[0][0], right=least_met_elems[1][0])] = a + b
        # print(d)
        return key_giver(d)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        temp = Counter(text)
        if keyword:
            text = vigineree(text, temp, keytext=keyword)
        temp = Counter(text)
        elems = dict()
        give = 0
        for k, v in temp.items():
            elems[Tree(value=k)] = v
            give = int(not give)

    keys = list(key_giver(elems).keys())[0]
    temp_dfs(keys)

    print(len(text))
    symbs = "".join([dictionary[_] for _ in text])
    text = "".join([(" " if k > 0 and k % 8 == 0 else "") + symbs[k] for k in range(len(symbs))])
    print(len(text))
    arr = text.split()

    chunks = [len(arr[-1])]
    chunks += list(map(lambda x: ord(x), json.dumps(dictionary)))
    print("dict", len(chunks))
    chunks += list(map(lambda x: int(x, 2), arr))
    chunks = bytes(chunks)
    print("full", len(chunks))

    with open(f"{path[:path.find('.')]}.par", "wb") as g:
        g.write(chunks)


def re_ixs(t):
    ixs = []
    for i in range(len(t)):
        if t[i] == "\\" and t[i + 2] != "u" and t[i + 2] != "n" and t[i + 1] != '"':
            ixs.append(i)

    t = "".join([char for idx, char in enumerate(t) if idx not in ixs]).replace('"""', "'" + '"' + "'")

    return t


def viginered(text, du, keytext):
    if not keytext:
        return text
    to = du["\u0b87"]
    del du["\u0b87"]
    du['"'] = to
    viginere = sorted(list(du.keys()))
    return ''.join(map(lambda x: viginere[viginere.index(x[0]) - ord(x[1]) % len(viginere)], zip(text, cycle(keytext))))


def decode(keyword=None):

    with open(path, "rb") as f:
        byte_data = f.read()

    bar = byte_data
    ln = bar[0]
    bar = bar[1:]
    text = str(bar)
    text = text[text.find("'") + 1:text.rfind("'")]

    call = text[text.find("{"):text.index("}") + 1].replace('"\\\\""', '"\u0b87"').replace("\\\\", "\\").replace("\\'", "'")
    rdictionary = json.loads(call)
    dictionary = {y: x for x, y in rdictionary.items()}
    print(dictionary)
    after_decoding = ""
    for byte in bar[bar.find(b"}") + 1:][:-1]:
        after_decoding += str(bin(byte))[2:].rjust(8, "0")
    after_decoding += str(bin(bar[-1]))[2:].rjust(8, "0")[-ln:]
    karret = 0
    cut = 0
    re = ""
    while cut < len(after_decoding):
        if after_decoding[karret:cut + 1] in dictionary:
            if dictionary[after_decoding[karret:cut + 1]] == "\u0b87":
                re += '"'
            else:
                re += dictionary[after_decoding[karret:cut + 1]]
            karret = cut
            karret += 1
        cut += 1

    with open(f"{path[:path.find('.')]}.txt", "w", encoding="utf-8") as f:
        if keyword:
            f.write(viginered(re, rdictionary, keytext=keyword))
        else:
            f.write(re)


if len(sys.argv) == 3:
    path = sys.argv[2]
    if sys.argv[1] == "-e":
        encode()
    elif sys.argv[1] == "-d":
        decode()
    else:
        raise BaseException("invalid parameters")
elif len(sys.argv) == 4:
    print(sys.argv[3])
    path = sys.argv[2]
    if sys.argv[1] == "-e":
        encode(sys.argv[3])
    elif sys.argv[1] == "-d":
        decode(sys.argv[3])
    else:
        raise BaseException("invalid parameters")
else:
    raise BaseException("invalid parameters")
