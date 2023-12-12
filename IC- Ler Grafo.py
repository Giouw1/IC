pasta = "asdasdad" #aqui inserir o path
def text_reader(texto):
    grafo = [] #lista que especifica o grafo
    aux = [] # Variável auxiliar, vai ajudar a construir a lista contendo as arestas e informações sobre o grafo
    teste = False
    for i in (texto):# melhorar complexidade? dá, e vale a pena percorrer TODO o texto antes, e partir do percorrido fazer isso
        for j in range(len(i)):
            try: # Caso seja um número de dois dígitos sendo lido
                if j+1 <= len(i):
                    int(i[j]) and int(i[j+1])
                else:
                    int(i[j])
                teste = True
            except:
                try: # Caso não seja um número de dois dígitos
                    int(i[j])
                except:
                    pass
                else:
                 if teste == False:
                        aux += [int(i[j])]
            else:
                aux += [int(i[j]+i[j+1])]
        if aux != []:
            grafo += [aux]
        aux = []
        teste = False
    return grafo
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

def faz_tudo(texto):
    texto_lido = text_reader(texto)
    matriz_final = matriz_adj(texto_lido)
    for i in range(len(matriz_final)):
        print(str(matriz_final[i])+"\n")
    return matriz_final
(faz_tudo(open(pasta)))
