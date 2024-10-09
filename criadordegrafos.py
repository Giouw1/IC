import networkx as nx
import random
from Leitor import matriz_adj
from Leitor import faz_tudo
#Completo é esparso com nvert*nvert-1 / 2 arestas
def cria_grafos():
    
    origem_grafo = input("Se for um grafo autoral, escreva autoral, se não, dê o tipo esparso,completo,bipartido_desbalanceado)")


    if origem_grafo == "autoral": #grafo.txt
        tipo_grafo = "esparso"
        try:
            open('grafo.txt',"r")
        except FileNotFoundError:
            print("Não há arquivo chamado 'grafo.txt', crie-o e digite o grafo que quiser")
        else:
            matriz_final= faz_tudo(open('grafo.txt'))

    else:
        qtd_vert = input("dê os vértices:")
        if origem_grafo == "completo":
            tipo_grafo = origem_grafo
            matriz_final = (esparso(int(qtd_vert),(int(qtd_vert)*(int(qtd_vert)-1))/2))
        elif origem_grafo == "esparso":
            tipo_grafo= origem_grafo
            qtd_arest= input("dê as arestas:")
            matriz_final = esparso(int(qtd_vert),int(qtd_arest))
        #posso adicionar aqui outras possibilidades de grafos
        elif origem_grafo == "bipartido_desbalanceado":
            tipo_grafo = origem_grafo
            matriz_final = bipartido_completos_desbalanceado(int(qtd_vert),int(int(qtd_vert)//3)*(int(qtd_vert)-int(int(qtd_vert)//3)))

        #Dado o grafo, processo para adquirir as informações adicionais necessárias pelo modelo.

    nedge = 0
    for i in range(len(matriz_final)-1): # só precisa ver até o vértice nvert-1, óbvio
        for j in range(i+1, len(matriz_final[i])):
            if matriz_final[i][j] == 1:
                nedge += 1
    nvert = len(matriz_final)

    #id_edge enumera as arestas, que são os elementos dos índices no arest.
    arest = []
    e = 0
    id_edge = [[-1 for j in range(nvert)] for i in range(nvert)]
    for i in range(nvert-1):        
        for j in range(i+1, len(matriz_final[i])):
            if matriz_final[i][j] == 1:
                id_edge[i][j] = id_edge[j][i] = e
                e += 1
                arest+=[(i,j)]
    return matriz_final, nedge, nvert,id_edge,arest,tipo_grafo

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
def bipartido_completos_desbalanceado(vertices,arestas):
    G = nx.complete_bipartite_graph(int(vertices//3),vertices-int(vertices//3))
    formato = list(G.edges())
    formato[0:0] = [(vertices,arestas)]
    return matriz_adj(formato)

