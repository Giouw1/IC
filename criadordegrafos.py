import networkx as nx
import random
from Leitor import matriz_adj
#Completo é esparso com nvert*nvert-1 / 2 arestas
def bipartido(vertices,arestas):
    #Dá erro quando o range 1 ou o range 2 go generator são 1 pois a biblioteca é definida dessa forma
    cut = random.randint(1,vertices-2) # Define o tamanho das "partições" aleatoriamente: Fazer grafo manual caso 1?
    G = nx.bipartite.gnmk_random_graph(cut,vertices-cut, arestas) #Testar depois
    formato = list(G.edges())
    formato[0:0] = [(vertices,arestas)]
    return matriz_adj(formato)
def esparso(vertices,arestas):
    G =  nx.gnm_random_graph(vertices,arestas)
    formato = list(G.edges())
    formato[0:0] = [(vertices,arestas)]
    return matriz_adj(formato)

