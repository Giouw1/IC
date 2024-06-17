import cplex
from Leitor import faz_tudo

def setupproblem(grafo, nedge, nvert, id_edge, arest):
    cpx = cplex.Cplex()
    #id_edge ordena as arestas, se id_edge[a][b] é 5, a aresta ab é a quinta
    lim_cam = 19*nvert
    numedge_sep = ((nedge*(nedge-1))//2)#Quantidade total de arestas que satisfaz f>e

    p = cpx.variables.add(obj=[1] * lim_cam,
                             lb=[0] * lim_cam, ub=[1] * lim_cam,
                             types=['B'] * lim_cam,
                             names=['p_%d' % (k) for k in range(1,lim_cam+1)])  

    x = [cpx.variables.add(obj=[0] * nedge,
                             lb=[0] *nedge, ub=[1] * nedge,
                             types=['B'] * nedge,
                             names=['x_%d_%d_%d' % (k,i,j)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1 ]) for k in range(1,lim_cam+1)]
    
    #arest é lista de arestas ordenada, poderia usar id edge para fazer a procura, mas precisaria de 4 iterações, evitei.
    se = [cpx.variables.add(obj=[0] *numedge_sep,
                            lb=[0] * numedge_sep, ub=[1] * numedge_sep,
                            types=['B'] * numedge_sep,                            
                            names=['sef_%d_%s_%s' % (k,arest[i],arest[j]) for i in range(nedge) for j in range((nedge)) if j>i]) for k in range(1,lim_cam+1)]
    sf = [cpx.variables.add(obj=[0] * numedge_sep,
                            lb=[0] * numedge_sep, ub=[1] * numedge_sep,
                            types=['B'] * numedge_sep,                            
                            names=['sfe_%d_%s_%s' % (k,arest[i],arest[j]) for i in range(nedge) for j in range((nedge)) if j<i]) for k in range(1,lim_cam+1)]

    #Restrição 1
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([p[k]]+[p[k+1]], [1.0,-1.0])
                  for k in range(lim_cam-1)],
        senses=['G'] * (lim_cam-1),
        rhs=[0.0] * (lim_cam-1) )

    #Restrição 2
    #id_edge ordena o x, para que, dada uma aresta, busque corretamente a variável x.
    #Como sei que, para cada caminho, tem nedge arestas, e que x[i] dá a iésima aresta, optei por não verificar se a aresta existe:se está em x, existe
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([x[k][i]]+[p[k]], [1.0,-1.0])
                  for k in range(lim_cam) for i in range(nedge)],
        senses=['L'] * lim_cam * nedge,
        rhs=[0.0] * lim_cam * nedge  )
    
    #Restrição 3
    #Sei que se, tem, para cada aresta e, todas as arestas f maiores que ela, e se é ordenado pelas arestas e
    #Logo, consigo chegar em uma dada aresta e, x[i], fazendo um cálculo de quantos elementos vieram anteriormente
    #Exemplo: Para e= (0,1), se inicia em 0, para (0,4) se inicia em 0 + todos os se com e sendo (0,1), (0,7) se inicia no início de (0,4)+ todos os se com e sendo (0,4)
    #A quantidade de elementos para cada e decresce em 1 por e, logo é uma p.a de -1. Fazendo a expressão, tenho o início do se com o e em questão
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([se[k][((i*(2*nedge-3-i))//2)+j]] + [x[k][i]], [1.0,-1.0])
                for k in range(lim_cam) for i in range(nedge) for j in range(i,nedge-1)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[0.0] * lim_cam * numedge_sep)
    #Mesma lógica do anterior, os sf são ordenados pelas arestas f, logo o número de elementos aumenta para cada f, e por isso a expressão abaixo
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([sf[k][((i*(i-1))//2)+j]] + [x[k][i]], [1.0,-1.0])
                for k in range(lim_cam)for i in range(1,nedge)for j in range(i)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[0.0] * lim_cam * numedge_sep)
    #Restrição 6
    #A mesma lógica da restrição anterior, mudança pequena, pois, para cada e, todos os f's, no primeiro caso, e o contrário no segundo
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([se[k][((i*(2*nedge-3-i))//2)+j]] + [x[k][j+1]], [1.0,1.0])
                  #Para cada f, encontra-se o e correspondente à x[i] na posição do f da aresta 0 +i
                for k in range(lim_cam)for i in range(0,nedge-1) for j in range(i,nedge-1)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[1.0] * lim_cam * numedge_sep) 
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([sf[k][((j*(j-1))//2)+i]] + [x[k][i]], [1.0,1.0])
                for k in range(lim_cam)for j in range(1,nedge) for i in range(j)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[1.0] * lim_cam * numedge_sep)

    #Restrição 7
    #Sem muitas complicações
    cpx.linear_constraints.add(
        lin_expr = [cplex.SparsePair([se[k][i]for i in range(numedge_sep)], [1.0]*numedge_sep)
        for k in range(lim_cam)],
        senses = ['G']*lim_cam,
        rhs=[1]*lim_cam)
    cpx.linear_constraints.add(
        lin_expr = [cplex.SparsePair([sf[k][i] for i in range(numedge_sep)], [1.0]*numedge_sep)
        for k in range(lim_cam)],
        senses = ['G']*lim_cam,
        rhs=[1]*lim_cam)
    sum = 0
    #Formulação MTZ:
    nedge_dir = (nedge + nvert)*2
    #Aqui vou formar o nome das variáveis a: Para facilitar a visualização, os nomes vao ser a uniao das listas a seguir
    names_1= ['a_%d_%d'% (-1,i) for i in range(nvert)]
    names_2= ['a_%d_%d'% (i,nvert) for i in range(nvert)]
    names_3= ['a_%d_%d'% (i,j)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1 ]
    names_4=['a_%d_%d'% (j,i)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1]
    print(len(names_1+names_2+names_3+names_4) == nedge_dir)

    a = [cpx.variables.add(obj=[0] * nedge_dir,
                             lb=[0] *nedge_dir, ub=[1] * nedge_dir,
                             types=['B'] * nedge_dir,
                             names=[['a_%d_%d_%d'% (k,-1,i) for i in range(nvert)] + ['a_%d_%d_%d'% (k,i,nvert) for i in range(nvert)] +['a_%d_%d_%d'% (k,i,j)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1 ] + ['a_%d_%d_%d'% (k,j,i)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1]]) for k in range(1,lim_cam+1)]
 #Lembrar que vai ter uma aresta inicial e uma final, para o direcionamento do grafo
    u = [cpx.variables.add(obj=[0] * nvert,
                             lb=[0] *nvert, ub=[nvert-1] * nvert,
                             names=['u_%d_%d' % (k,i)  for i in range(nvert)]) for k in range(1,lim_cam+1)]
    #Restrição 8
    cpx.linear_constraints.add(

        lin_expr = [cplex.SparsePair([], [1,1,-1])
        for k in range(lim_cam) ],
        senses = ['E']*nedge*lim_cam,
        rhs=[0]*nedge*lim_cam)

    
    cpx.write('model.lp')  # Escreve o modelo em um arquivo LP
#    cpx.linear_constraints.add(
 #   O LADO ESQUERDO    lin_expr=[cplex.SparsePair()
  #                for i in range(vertices)],
   #    G, L, E, R(anged) senses=[] * vertices,
    #  DIREITA  rhs=[0.0] * vertices)


matriz_final, nedge, nvert, id_edge, ef_aux = faz_tudo(open(r'C:/Users/Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\grafo.txt'))
setupproblem(matriz_final, nedge, nvert,id_edge,ef_aux)
