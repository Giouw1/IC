from Leitor import faz_tudo
from CPXGRAPHSOLVER import setupproblem
from criadordegrafos import esparso
from criadordetabela import cria_tabela
#Preciso ver se os arquivos que estou usando existem e, caso n'ao existam,criar. VER ISSO NO AUTYORAL, DADOS, TABELA
#Os grafos são do tipo list, e não classe própria.

origem_grafo = input("Se for um grafo autoral, escreva autoral, se não, dê o tipo esparso,completo)")


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
        tipo_grafo = "completo"
        matriz_final = (esparso(int(qtd_vert),(int(qtd_vert)*(int(qtd_vert)-1))/2))
    elif origem_grafo == "esparso":
        tipo_grafo= "esparso"
        qtd_arest= input("dê as arestas:")
        matriz_final = esparso(int(qtd_vert),int(qtd_arest))
    #posso adicionar aqui outras possibilidades de grafos

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

#Cria o arquivo dados.txt caso não exista
try:
    open("dados.txt", "r")
except FileNotFoundError:
    a = open("dados.txt","x")
    a.close()
setupproblem(matriz_final, nedge, nvert,id_edge,arest,tipo_grafo)

#Cria o arquivo tabelas.csv caso não exista
try:
    open("tabelas.csv", "r")
except FileNotFoundError:
    a = open("tabelas.csv","x")
    a.close()
    cria_tabela(open('dados.txt'),'tabelas.csv', 'tabelas.csv')

#Intuito de limpar o arquivo de dados
with open (r'c:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\dados.txt', "w") as file:
    pass
