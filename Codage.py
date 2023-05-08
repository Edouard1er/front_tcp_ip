import os

class element:
    def __init__(self, occurence):
        self.occurence = occurence

    def __repr__(self) -> str:
        return str(self.occurence)


class feuille(element):
    def __init__(self, caractere, occurence):
        super().__init__(occurence)
        self.caractere = caractere

    def __repr__(self) -> str:
        return f' caractere : {self.caractere} occurence : ' + super().__repr__()


class noeud(element):
    def __init__(self, gauche: element, droite: element):
        super().__init__(gauche.occurence + droite.occurence)
        self.gauche = gauche
        self.droite = droite

    def __repr__(self) -> str:
        return super().__repr__()

class HuffmanCode:
    def __init__(self, file_name):
        self.huffman_list = None
        self.huffman_dict = None
        self.huffman_tree = None
        self.init_tree(file_name)

    def init_tree(self, file_name):
        self.huffman_tree = self.create_list(file_name)
        self.huffman_list = self.create_tree(self.huffman_tree)
        self.huffman_dict = {}
        self.create_code(self.huffman_list[0], "", self.huffman_dict)

    @staticmethod
    def create_list(file_name):
        folder_path = 'static/files'
        file_path = os.path.join(folder_path, file_name)

        fichier = open(file_path, "rb")
        data = fichier.read().decode()
        lst = []

        while len(data) > 0:
            caractere = data[0]
            occurence = data.count(caractere)
            data = data.replace(caractere, '')
            lst.append(feuille(caractere, occurence))
        return sorted(lst, key=lambda elements: elements.occurence, reverse=True)

    @staticmethod
    def create_tree(tree: list):
        while len(tree) > 1:
            elem1 = tree.pop(-1)
            elem2 = tree.pop(-1)
            tree.append(noeud(elem1, elem2))
            tree = sorted(tree, key=lambda elements: elements.occurence, reverse=True)
        return tree

    @staticmethod
    def create_code(e: element, code: str, dic: dict):
        if type(e) is feuille:
            dic[e.caractere] = code
        else:
            code += str(0)
            HuffmanCode.create_code(e.gauche, code, dic)
            code = code[:-1]
            code += str(1)
            HuffmanCode.create_code(e.droite, code, dic)
            code = code[:-1]
        return dic

    def get_huffman_list(self):
        return self.huffman_list

    def get_huffman_dict(self):
        return self.huffman_dict

    def get_huffman_tree(self):
        return self.huffman_tree


def compressFile(dico, filename):
    dataBin = ''
    folder_path = 'static/files'
    file_path = os.path.join(folder_path, filename)

    fichier = open(file_path, "rb")
    data = fichier.read().decode()

    for char in data:
        dataBin = dataBin + dico[char]
    complement = (8 - len(dataBin) % 8)
    if complement > 0:
        dataBin = dataBin + '0' * complement
    dataCompress = chr(complement)
    length = int(len(dataBin) / 8)
    D = 0
    for i in range(length):
        dataCompress = dataCompress + chr(int(dataBin[D:D + 8], 2))
        D += 8

    return dataCompress


def decompressData(compressed_data: str, node):
    complement = ord(compressed_data[0])
    compressed_data = compressed_data[1:]
    print("test")

    binary_data = ''.join([bin(ord(char))[2:].rjust(8, '0') for char in compressed_data])
    binary_data = binary_data[:-complement]

    decompressed_data = ''
    current_node = node
    for bit in binary_data:
        if bit == '0':
            current_node = current_node.gauche
        elif bit == '1':
            current_node = current_node.droite

        if isinstance(current_node, feuille):
            decompressed_data += current_node.caractere
            current_node = node
    print("TEST 123")
    return decompressed_data
