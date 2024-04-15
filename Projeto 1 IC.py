#adicionar variaveis, adicionair constraints, e resolver.
#variaveis sao os nos do grafo q vou ler
import cplex
from Leitor import faz_tudo



grafo = (faz_tudo(open(r'C:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\grafo.txt')))
#colocar o endereço do grafo.txt
vertices = len(grafo)
#as arestas sao 1 ou 0(existem ou nao) em grafo[1no][2no]
#Quero que haja pares de caminhos que separem todas as arestas, quantidade de pares de caminhos para que todas as combinacoes 2 a 2 de arestas sejam separadas é a psn(G)
def setupproblem(c, grafo, nedge):
    cpx = cplex.Cplex()
    
    nvert = len(grafo)
    lim_cam = 19*nvert

    e = 0
    id_edge = [[-1 for j in range(nvert)] for i in range(nvert)]
    for i in range(nvert-1):        
        for j in range(i+1, nvert):
            if grafo[i][j] == 1:
                id_edge[i][j] = id_edge[j][i] = e
                e += 1
    
    p = cpx.variables.add(obj=[1] * lim_cam,
                             lb=[0] * lim_cam, ub=[1] * lim_cam,
                             types=['B'] * lim_cam,
                             names=['p_%d' % (k) for k in range(1,lim_cam+1)])

    x = [cpx.variables.add(obj=[0] * nedge,
                             lb=[0] *nedge, ub=[1] * nedge,
                             types=['B'] * nedge,
                             names=['x^%d_%d_%d' % (k,i,j)  for i in range(nvert-1) for j in range(i+1,nvert) if grafo[i][j] == 1 ]) for k in range(1,lim_cam+1)]
                             
    #Restrição 2
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([p[k]]+[p[k+1]], [1.0,-1.0])
                  for k in range(lim_cam-1)],
        senses=['G'] * (lim_cam-1),
        rhs=[0.0] * (lim_cam-1) )

    #Restrição 3
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([x[k][id_edge[i][j]]+[p[k]], [1.0,-1.0])
                  for k in range(lim_cam) for i in range(nvert-1) for j in range(i+1,nvert) if grafo[i][j] == 1],
        senses=['L'] * lim_cam * nedge,
        rhs=[0.0] * lim_cam * nedge  )

    cpx.write('model.lp')  # Escreve o modelo em um arquivo LP
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
