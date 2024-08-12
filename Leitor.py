def matriz_adj(texto_lido):
    matriz_f = []
    for k in range(texto_lido[0][0]):#quantidade de vertices
        matriz_f += [[0]*texto_lido[0][0]]
    for i in range(1,len(texto_lido)):
        matriz_f[texto_lido[i][0]][texto_lido[i][1]] = 1
        matriz_f[texto_lido[i][1]][texto_lido[i][0]] = 1
    return matriz_f
def text_reader(texto):
    auxiliar = []
    marcador = 0
    grafo= []
    for i in (texto):
        if i == " " or i == "end":
            break
        for j in range(len(i)):
            if (i[j]) == " " and marcador == 0:
                marcador = 1
                auxiliar += [int(i[0:j])]
                continue
            elif (i[j]) == " " and marcador == 1:
                auxiliar += [int(i[j+1:(len(i)-1)] )]
                marcador = 0
        print(auxiliar)
        grafo +=[auxiliar]
        auxiliar = []
    return grafo
def faz_tudo(texto):
    texto_lido = text_reader(texto)
    print(texto_lido)
    matriz_final = matriz_adj(texto_lido)
    nedge = 0
    for i in range(len(matriz_final)-1): # só precisa ver até o vértice nvert-1, óbvio
        for j in range(i+1, len(matriz_final[i])):
            if matriz_final[i][j] == 1:
                nedge += 1
    nvert = len(matriz_final)
    e = 0
    #id edge simplesmente enumera as arestas existentes
    #lista de arestas arest
    arest = []
    id_edge = [[-1 for j in range(nvert)] for i in range(nvert)]
    for i in range(nvert-1):        
        for j in range(i+1, len(matriz_final[i])):
            if matriz_final[i][j] == 1:
                id_edge[i][j] = id_edge[j][i] = e
                e += 1
                arest+=[(i,j)]
                    
    return matriz_final, nedge, nvert, id_edge, arest
#Formato do grafo tem que ser:
# 1 linha (número de vértices), (número de arestas)
# para cada linha, aresta: vérticeA - vérticeB, dessa exata maneira.
