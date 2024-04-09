#adicionar variaveis, adicionair constraints, e resolver.
#variaveis sao os nos do grafo q vou ler
import cplex
from Leitor import faz_tudo

grafo = (faz_tudo(open(r'C:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\grafo.txt')))
vertices = len(grafo)
print(grafo)
#as arestas sao 1 ou 0(existem ou nao) em grafo[1no][2no]
#Quero que haja pares de caminhos que separem todas as arestas
def setupproblem(c):
    c = cplex.Cplex()
    #Qual nome colocar?
    familia_caminhos = c.variables.add(lb = [0]*(vertices*19), ub = [1]*(vertices*19),
                                       types = ['B']*(vertices*19)) #Isso é PK
    # a questão agora é pensar em como organizar as variaveis de caminho, e as de separação:
    #tem que ter duas variáveis para caminho, dois caminhos, contendo arestas a e b, que os separem
    #estou criando mais variavel do que o necessario
#    cpx.linear_constraints.add(
 #   O LADO ESQUERDO    lin_expr=[cplex.SparsePair([h[i]]+[y[i]], [1.0,-1.0])
  #                for i in range(vertices)],
   #    G, L, E, R(ANGED) senses=['L'] * vertices,
    #  DIREITA  rhs=[0.0] * vertices)