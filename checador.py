import networkx as nx
import matplotlib.pyplot as plt
# O que é/ O que quero fazer com o checador? Mostrar o grafo: Cada um dos caminhos: um conjunto de grafos: posso deixar a opção de escrever um arquivo com o grafo, etc, p/facilitar as coisas

def checar(nvert):
    texto = open('solucao.txt',"r")
    caminhos = le_caminho(texto)
    dicionario_grafos = {}
    for i in range (len(caminhos)):
        dicionario_grafos[f'G_{i}'] = nx.Graph()
        dicionario_grafos[f'G_{i}'].add_nodes_from(range(nvert))
        for j in range(0,len(caminhos[i]),2):
            dicionario_grafos[f'G_{i}'].add_edge(caminhos[i][j],caminhos[i][j+1])
    for i in range (len(caminhos)):
        nx.draw(dicionario_grafos[f'G_{i}'], with_labels =True)   
        plt.show()      
    
def le_caminho(texto):
    caminhos = []
    for line in texto:
        if line[0] == "s":break
        if line[0] == "x":
            caminho_at=-1
            for i in range(len(line)):
                if line[i] == "_":
                    for j in range(i+1,len(line)):
                        if line[j] == "_" or line[j] == " ":
                            if caminho_at == -1:
                                caminho_at = int(line[i+1:j])-1
                                break
                            else: caminhos[caminho_at] += [int(line[i+1:j])];break
        else:
            caminhos += [[]]
    return caminhos
print(checar(4))                    