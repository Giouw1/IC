from Leitor import faz_tudo
from resolvedorcpx import setupproblem
from criadordegrafos import cria_grafos
from criadordetabela import cria_tabela
from checador import checar
#LIMITANTE SUPERIOR: NUMERO DE ARESTAS, 2N PRA GRAFO COMPLETO, 3N PRA GRAFO PLANAR
#Algoritmo para visualizar se ta certo: checador, e ver os paths
#networkx, utilizar cada caminho como um grafo pra ver as especializacoes

matriz_final, nedge, nvert,id_edge,arest,tipo_grafo = cria_grafos()

setupproblem(matriz_final, nedge, nvert,id_edge,arest,tipo_grafo)

#Cria o arquivo tabelas.csv caso não exista
try:
    open("tabelas.csv", "r")
except FileNotFoundError:
    a = open("tabelas.csv","x")
    a.close()
    cria_tabela(open('dados.txt'),'tabelas.csv', 'tabelas.csv')
else: cria_tabela(open('dados.txt'),'tabelas.csv', 'tabelas.csv')
#Intuito de limpar o arquivo de dados
with open ('dados.txt', "w") as file:
    pass
desejo_checa = input("Deseja checar cada caminho? (1/0 = S/N)")
if desejo_checa == 1:
    checar(nvert)
