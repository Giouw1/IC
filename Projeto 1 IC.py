#adicionar variaveis, adicionair constraints, e resolver.
#variaveis sao os nos do grafo q vou ler
import cplex
from Leitor import faz_tudo



grafo = (faz_tudo(open(r'C:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\grafo.txt')))
#colocar o endereço do grafo.txt
vertices = len(grafo)
#as arestas sao 1 ou 0(existem ou nao) em grafo[1no][2no]
#Quero que haja pares de caminhos que separem todas as arestas, quantidade de pares de caminhos para que todas as combinacoes 2 a 2 de arestas sejam separadas é a psn(G)
def setupproblem(c, grafo):
    c = cplex.Cplex()
    
    nvert = len(grafo)
    lim_cam = 19*nvert
    
    p = cpx.variables.add(obj=[1] * lim_cam,
                             lb=[0] * lim_cam, ub=[1] * lim_cam,
                             types=['B'] * lim_cam,
                             names=['p_%d' % (p) for p in range(1,lim_cam+1)])
                             
    #Restrição 2
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([p[i]]+[p[i+1]], [1.0,-1.0])
                  for i in range(lim_cam-1)],
        senses=['G'] * (lim_cam-1),
        rhs=[0.0] * (lim_cam-1)                     
    #Qual nome colocar?
    #familia_caminhos = c.variables.add(lb = [0]*(vertices*19), ub = [1]*(vertices*19),
                                      # types = ['B']*(vertices*19)) #Isso é PK
    # a questão agora é pensar em como organizar as variaveis de caminho, e as de separação:
    #
#    cpx.linear_constraints.add(
 #   O LADO ESQUERDO    lin_expr=[cplex.SparsePair()
  #                for i in range(vertices)],
   #    G, L, E, R(anged) senses=[] * vertices,
    #  DIREITA  rhs=[0.0] * vertices)
