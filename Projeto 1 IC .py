
import cplex
from criadordegrafos import esparso
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
    s = [cpx.variables.add(obj=[0] *2*numedge_sep,
                            lb=[0] * 2*numedge_sep, ub=[1] * 2*numedge_sep,
                            types=['B'] * 2*numedge_sep,                            
                            names=['s_%d_%s_%s' % (k,arest[i],arest[j]) for i in range(nedge) for j in range((nedge)) if j>i]+['s_%d_%s_%s' % (k,arest[j],arest[i]) for i in range(nedge) for j in range((nedge)) if j>i]) for k in range(1,lim_cam+1)]
  

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
        rhs=[0.0] * lim_cam * nedge)
    
    #Restrição 3
    #Sei que se, tem, para cada aresta e, todas as arestas f maiores que ela, e se é ordenado pelas arestas e
    #Logo, consigo chegar em uma dada aresta e, x[i], fazendo um cálculo de quantos elementos vieram anteriormente
    #Exemplo: Para e= (0,1), se inicia em 0, para (0,4) se inicia em 0 + todos os se com e sendo (0,1), (0,7) se inicia no início de (0,4)+ todos os se com e sendo (0,4)
    #O controle de fluxo tem que ter os vértices adicionados?
    #A quantidade de elementos para cada e decresce em 1 por e, logo é uma p.a de -1. Fazendo a expressão, tenho o início do se com o e em questão
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((i*(2*nedge-3-i))//2)+j]] + [x[k][i]], [1.0,-1.0])
                for k in range(lim_cam) for i in range(nedge) for j in range(i,nedge-1)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[0.0] * lim_cam * numedge_sep)
    #Mesma lógica do anterior, os sf são ordenados pelas arestas f, logo o número de elementos aumenta para cada f, e por isso a expressão abaixo
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((i*(i-1))//2)+j]+numedge_sep] + [x[k][i]], [1.0,-1.0])
                for k in range(lim_cam)for i in range(1,nedge)for j in range(i)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[0.0] * lim_cam * numedge_sep)
    #Restrição 6
    #A mesma lógica da restrição anterior, mudança pequena, pois, para cada e, todos os f's, no primeiro caso, e o contrário no segundo
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((i*(2*nedge-3-i))//2)+j]] + [x[k][j+1]], [1.0,1.0])
                  #Para cada f, encontra-se o e correspondente à x[i] na posição do f da aresta 0 +i
                for k in range(lim_cam)for i in range(0,nedge-1) for j in range(i,nedge-1)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[1.0] * lim_cam * numedge_sep) 
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((j*(j-1))//2)+i]+numedge_sep] + [x[k][i]], [1.0,1.0])
                for k in range(lim_cam)for j in range(1,nedge) for i in range(j)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[1.0] * lim_cam * numedge_sep)

    #Restrição 7
    #Sem muitas complicações
    cpx.linear_constraints.add(
        lin_expr = [cplex.SparsePair([s[k][i]for k in range(lim_cam)], [1.0]*lim_cam)
        for i in range(numedge_sep)],
        senses = ['G']*numedge_sep,
        rhs=[1]*numedge_sep)
    cpx.linear_constraints.add(
        lin_expr = [cplex.SparsePair([s[k][i+numedge_sep] for k in range(lim_cam)], [1.0]*lim_cam)
        for i in range(numedge_sep)],
        senses = ['G']*numedge_sep,
        rhs=[1]*numedge_sep)



    #Formulação MTZ:
    nedgesout_per_vert = [] # Quantas arestas saem por vértice
    for i in range(len(grafo)):
        counter = 0
        for j in range(i,len(grafo[i])):
            if grafo[i][j] == 1:counter +=1
        nedgesout_per_vert += [counter]
    nedgesin_per_vert = [] # Quantas arestas "entram" para cada vértice (tem o vértice do lado "direto")
    for i in range(len(grafo)):
        counter = 0
        for j in range(0,i):
            if grafo[i][j] == 1:counter +=1
        nedgesin_per_vert += [counter]
    nedge_dir = (nedge + nvert)*2
    #Aqui vou formar o nome das variáveis a: Para facilitar a visualização, os nomes vao ser a uniao das listas a seguir
    names_1= ['a_%d_%d'% (-1,i) for i in range(nvert)]
    names_2= ['a_%d_%d'% (i,nvert) for i in range(nvert)]
    names_3= ['a_%d_%d'% (i,j)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1 ]
    names_4= ['a_%d_%d'% (j,i)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1]
    a = [cpx.variables.add(obj=[0] * nedge_dir,
                             lb=[0] *nedge_dir, ub=[1] * nedge_dir,
                             types=['B'] * nedge_dir,
                             names=['a_%d_-1_%d'% (k,i) for i in range(nvert)] + ['a_%d_%d_%d'% (k,i,nvert) for i in range(nvert)] +['a_%d_%d_%d'% (k,i,j)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1 ] + ['a_%d_%d_%d'% (k,j,i)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1]) for k in range(1,lim_cam+1)]
 #Lembrar que vai ter uma aresta inicial e uma final, para o direcionamento do grafo
    u = [cpx.variables.add(obj=[0] * nvert,
                             lb=[0] *nvert, ub=[nvert-1] * nvert,
                             names=['u_%d_%d' % (k,i)  for i in range(nvert)]) for k in range(1,lim_cam+1)]
    #Restrição 8
    #a é organizado em todos de -1 até vert (de tamanho nvert), todos vert até nvert+1(nvert), ordem de arestas normal e ao contrário.
    cpx.linear_constraints.add(

        lin_expr = [cplex.SparsePair([a[k][i+2*nvert]] + [a[k][i+2*nvert+nedge]] + [x[k][i]], [1,1,-1])
        for k in range(lim_cam)  for i in range(nedge) ],
        senses = ['E']*nedge*lim_cam,
        rhs=[0]*nedge*lim_cam)

    #Restrição 9
    cpx.linear_constraints.add(
        lin_expr = [cplex.SparsePair([a[k][i]] + [a[k][id_edge[i][j]+2*nvert+nedge]for j in range(i,len(grafo[i])) if id_edge[i][j] != -1] + [a[k][id_edge[j][i]+2*nvert] for j in range(i) if id_edge[j][i] != -1] + [u[k][i]], [1]+[2]*nedgesout_per_vert[i] + [2]*nedgesin_per_vert[i] + [-1])
        for k in range(lim_cam)  for i in range(nvert)],
        senses = ['L']*nvert*lim_cam,
        rhs=[0]*nvert*lim_cam)
    #Restrição 10
    cpx.linear_constraints.add(
        lin_expr = [cplex.SparsePair([u[k][i]]+ [p[k]] + [a[k][i]] , [1,-(nvert-1),nvert-2])
        for k in range(lim_cam) for i in range(nvert)],
        senses = ['L']*lim_cam*nvert,
        rhs=[0]*lim_cam*nvert)
    #Restrição 11
    cpx.linear_constraints.add(
       lin_expr = [cplex.SparsePair([a[k][i]]+[a[k][id_edge[i][j]+2*nvert+nedge]for j in range(i,len(id_edge[i])) if id_edge[i][j] != -1] + [a[k][id_edge[j][i]+2*nvert] for j in range(i) if id_edge[j][i] != -1] + [a[k][id_edge[i][j]+2*nvert] for j in range(i,len(id_edge[i])) if id_edge[i][j] != -1] + [a[k][id_edge[j][i]+2*nvert+nedge] for j in range(i) if id_edge[j][i] != -1]+ [a[k][i+nvert]], [1] + [1]*(nedgesout_per_vert[i]+nedgesin_per_vert[i])+ [-1]*(nedgesout_per_vert[i]+nedgesin_per_vert[i])+ [-1])
       for k in range(lim_cam) for i in range(nvert) ],
       senses = ['E']*lim_cam*nvert,
       rhs=[0]*lim_cam*nvert)
    
    #Restrição 12
    #Só pode entrar 1 vez no vértice por caminho: Evita ciclos
    cpx.linear_constraints.add(

       lin_expr = [cplex.SparsePair([a[k][id_edge[i][j]+2*nvert+nedge]for j in range(i,len(grafo[i])) if id_edge[i][j] != -1] + [a[k][id_edge[j][i]+2*nvert] for j in range(i) if id_edge[j][i] != -1]+ [p[k]], [1]*nedgesout_per_vert[i] + [1]*nedgesin_per_vert[i] + [-1])
       for k in range(lim_cam) for i in range(nvert)],
       senses = ['L']*lim_cam*nvert,
       rhs=[0]*lim_cam*nvert)
    #Só pode ter 1 começo e 1 final.
    #Restrição 15
    cpx.linear_constraints.add(

       lin_expr = [cplex.SparsePair([a[k][i] for i in range(nvert)]+[p[k]], [1]*nvert+[-1])
       for k in range(lim_cam)],
       senses = ['E']*lim_cam,
       rhs=[0]*lim_cam)
    #Restrição 16
    cpx.linear_constraints.add(

       lin_expr = [cplex.SparsePair([a[k][i+nvert] for i in range(nvert)]+[p[k]], [1]*nvert+[-1])
       for k in range(lim_cam)],
       senses = ['E']*lim_cam,
       rhs=[0]*lim_cam)
    #Restrição 17

    cpx.linear_constraints.add(

       lin_expr = [cplex.SparsePair([u[k][i]] + [u[k][j]] + [p[k]]+ [a[k][2*nvert +id_edge[i][j]]]+ [a[k][2*nvert+nedge+id_edge[i][j]]], [-1]+[1]+[2-nvert]+[nvert-3]+[nvert-1])
       for k in range(lim_cam) for i in range(nvert) for j in range(i,nvert) if id_edge[i][j] != -1],
       senses = ['L']*lim_cam*nedge,
       rhs=[0]*lim_cam*nedge)
    cpx.objective.set_sense(cpx.objective.sense.minimize)
    cpx.write('model.lp')  # Escreve o modelo em um arquivo LP
    cpx.solve()
#Testar o código, ver restrição por restrição, e apósa isso testar um grafo.
#    print('Solution status:                   %d' % cpx.solution.get_status())
#ESCREVA O PATH DO SEU SOLUTION TXT PARA PODER OBTER AS SOLUÇÕES
    variable_names = cpx.variables.get_names()
    variable_values = cpx.solution.get_values()
    ver_var = []
    for var_name, var_value in zip(variable_names, variable_values):
        ver_var+=[f"{var_name} = {var_value}"]
    with open(r'C:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\solucao.txt' , 'w') as f:
        for i in ver_var:
            f.write(i+'\n')


origem_grafo = input("Se for um grafo autoral, escreva autoral, se não, dê o tipo esparso,completo)")
if origem_grafo == "autoral": #ESCREVA A PATH DO SEU GRAFO AUTORAL
    matriz_final, nedge, nvert, id_edge, ef_aux = faz_tudo(open(r'c:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\grafo.txt'))
else:
    qtd_vert = input("dê os vértices:")
    if origem_grafo == "completo":
        
        matriz_final = (esparso(int(qtd_vert),(qtd_vert*(qtd_vert-1))/2))
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
    if origem_grafo == esparso:
        qtd_arest= input("dê as arestas:")
        matriz_final = esparso(qtd_vert,qtd_arest)
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
#AGORA, EXTRAIR INFORMAÇÕES DO GRAFO
 
#else: pass
print(matriz_final)
setupproblem(matriz_final, nedge, nvert,id_edge,ef_aux)
#Escrever informações em um txt e separa-las por ;.
#nome da instancia, relaxacao linear(tenho q ver como pegar), numero de nos, best integer, best bound, tempo total
#c:\Users\Gio Faletti\Documents\GioPosEscola\ic\codigos\ProgVS\grafo.txt
