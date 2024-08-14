from Leitor import faz_tudo
from CPXGRAPHSOLVER import setupproblem
from criadordegrafos import esparso
from criadordetabela import cria_tabela
#Os grafos são do tipo list, e não classe própria.

origem_grafo = input("Se for um grafo autoral, escreva autoral, se não, dê o tipo esparso,completo)")
if origem_grafo == "autoral": #ESCREVA A PATH DO SEU GRAFO AUTORAL
    tipo_grafo = "esparso"
    matriz_final, nedge, nvert, id_edge, ef_aux = faz_tudo(open(r'c:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\grafo.txt'))
else:
    qtd_vert = input("dê os vértices:")
    if origem_grafo == "completo":
        tipo_grafo = "completo"
        matriz_final = (esparso(int(qtd_vert),(qtd_vert*(qtd_vert-1))/2))
    elif origem_grafo == "esparso":
        tipo_grafo= "esparso"
        qtd_arest= input("dê as arestas:")
        matriz_final = esparso(int(qtd_vert),int(qtd_arest))
    #posso adicionar aqui outras possibilidades de grafos
    nedge = 0
    for i in range(len(matriz_final)-1): # só precisa ver até o vértice nvert-1, óbvio
        for j in range(i+1, len(matriz_final[i])):
            if matriz_final[i][j] == 1:
                nedge += 1
    nvert = len(matriz_final)
    ef_aux = []
    e = 0
    id_edge = [[-1 for j in range(nvert)] for i in range(nvert)]
    for i in range(nvert-1):        
        for j in range(i+1, len(matriz_final[i])):
            if matriz_final[i][j] == 1:
                id_edge[i][j] = id_edge[j][i] = e
                e += 1
                ef_aux+=[(i,j)]
setupproblem(matriz_final, nedge, nvert,id_edge,ef_aux,tipo_grafo)
#Precisa de um arquivo para dados, um arquivo para tabela.csv,grafo.txt, e model lp
cria_tabela(open(r'c:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\dados.txt'),r'c:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\tabelas.csv', r'c:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\tabelas.csv')
#Limpo o arquivo de dados após isso
with open (r'c:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\dados.txt', "w") as file:
    pass
#Posso deixar para rodar aqui várias vezes, todas elas vão ser escritas no dados.txt, e posso usar isso depois