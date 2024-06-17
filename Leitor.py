def matriz_adj(texto_lido):
    matriz_f = []
    for k in range(texto_lido[0][0]):#quantidade de vertices
        matriz_f += [[]]
        #se for maior, do que o o tamanho atual, enche de 0`s ate o valor em questao e preenche o bloco, se nao, so preenche o bloco com `1`
    for i in range(1,len(texto_lido)):
        maior = 0
        for j in range(1,len(texto_lido)):
            if texto_lido[j][0] == i:
                if texto_lido[j][1]>=maior:
                    for k in range(texto_lido[j][1]-maior):
                        matriz_f[i-1]+=[0]
                    maior = texto_lido[j][1]
                matriz_f[i-1][texto_lido[j][1]-1] = 1
            elif texto_lido[j][1] == i:
                if texto_lido[j][0]>=maior:
                    for n in range(texto_lido[j][0]-maior):
                        matriz_f[i-1]+=[0]
                    maior = texto_lido[j][0]
                matriz_f[i-1][texto_lido[j][0]-1] = 1
    return matriz_f
def text_reader(texto):
    auxiliar = []
    marcador = 0
    grafo= []
    for i in (texto):
        if i == " ":
            break
        for j in range(len(i)):
            if (i[j]) == " " and marcador == 0:
                marcador = 1
                auxiliar += [int(i[0:j])]
                continue
            elif (i[j]) == " " and marcador == 1:
                auxiliar += [int(i[j+1:(len(i)-1)])]
                marcador = 0
        grafo +=[auxiliar]
        auxiliar = []
    return grafo
def faz_tudo(texto):
    texto_lido = text_reader(texto)
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
