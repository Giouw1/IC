
import cplex
from criadordegrafos import esparso
from Leitor import faz_tudo
#Grafo completo: 2n
# Grafo planar
#regulares e semiregulares
#grafo cubico

def setupproblem(grafo, nedge, nvert, id_edge, arest,tipo_grafo):
    cpx = cplex.Cplex()

    #id_edge ordena as arestas, se id_edge[a][b] é 5, a aresta ab é a quinta
    if tipo_grafo == "completo":
        lim_cam = min(2*nvert,nedge)
    else:
        lim_cam = min(19*nvert,nedge)
    numedge_sep = ((nedge*(nedge-1))//2)#Quantidade total de arestas que satisfaz f>e

    p = cpx.variables.add(obj=[1] * lim_cam,
                             lb=[0] * lim_cam, ub=[1] * lim_cam,
                             types=['B'] * lim_cam,
                             names=['p_%d' % (k) for k in range(1,lim_cam+1)])  

    x = [cpx.variables.add(obj=[0] * nedge,
                             lb=[0] *nedge, ub=[1] * nedge,
                             types=['B'] * nedge,
                             names=['x_%d_%d_%d' % (k,i,j)  for i in range(nvert-1) for j in range(i+1,len(grafo[i])) if grafo[i][j] == 1 ]) for k in range(1,lim_cam+1)]
    #arest é lista de arestas ordenada.
    s = [cpx.variables.add(obj=[0] *2*numedge_sep,
                            lb=[0] * 2*numedge_sep, ub=[1] * 2*numedge_sep,
                            types=['B'] * 2*numedge_sep,                            
                            names=['s_%d_%s_%s' % (k,arest[i],arest[j]) for i in range(nedge) for j in range((nedge)) if j>i]+['s_%d_%s_%s' % (k,arest[j],arest[i]) for j in range(nedge) for i in range((nedge)) if j>i]) for k in range(1,lim_cam+1)]
  

    #Restrição 1
    #Ordena os caminhos à serem utilizados
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([p[k]]+[p[k+1]], [1.0,-1.0])
                  for k in range(lim_cam-1)],
        senses=['G'] * (lim_cam-1),
        rhs=[0.0] * (lim_cam-1) )

    #Restrição 2
    #Só posso usar a aresta caso exista o caminho
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([x[k][i]]+[p[k]], [1.0,-1.0])
                  for k in range(lim_cam) for i in range(nedge)],
        senses=['L'] * lim_cam * nedge,
        rhs=[0.0] * lim_cam * nedge)
    
    #Restrição 3
    #As expressões utilizadas para buscar os s's corretos é dada pelo fato de que só posso usar f>e, maior o e, menos f disponíveis: padrão que me fez pegar os s's corretos
    # Se contem a aresta ij, pode separar a aresta ij da aresta uv

    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((i*(2*nedge-3-i))//2)+j]] + [x[k][i]], [1.0,-1.0])
                for k in range(lim_cam) for i in range(nedge) for j in range(i,nedge-1)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[0.0] * lim_cam * numedge_sep)
    
    #Se contém a aresta uv,pode separar a aresta uv da aresta ij

    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((i*(i-1))//2)+j]+numedge_sep] + [x[k][i]], [1.0,-1.0])
                for k in range(lim_cam)for i in range(1,nedge)for j in range(i)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[0.0] * lim_cam * numedge_sep)
    
    
    #Para todo caminho, se ele separa as arestas, indicar isso (força a existência do s caso haja a separação)

    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((i*(2*nedge-3-i))//2)+j]] + [x[k][i]]+ [x[k][j+1]], [1.0,-1.0,1.0])
                for k in range(lim_cam) for i in range(nedge) for j in range(i,nedge-1)],
        senses=['G'] * lim_cam * numedge_sep,
        rhs=[0.0] * lim_cam * numedge_sep)
    
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((i*(i-1))//2)+j]+numedge_sep] + [x[k][i]] + [x[k][j]], [1.0,-1.0,1.0])
                for k in range(lim_cam)for i in range(1,nedge)for j in range(i)],
        senses=['G'] * lim_cam * numedge_sep,
        rhs=[0.0] * lim_cam * numedge_sep)
    

    #Restrição 6
    #Mesma lógica da resitrção 4, só que ao contrário
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((i*(2*nedge-3-i))//2)+j]] + [x[k][j+1]], [1.0,1.0])
                for k in range(lim_cam)for i in range(0,nedge-1) for j in range(i,nedge-1)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[1.0] * lim_cam * numedge_sep) 
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([s[k][((j*(j-1))//2)+i]+numedge_sep] + [x[k][i]], [1.0,1.0])
                for k in range(lim_cam)for j in range(1,nedge) for i in range(j)],
        senses=['L'] * lim_cam * numedge_sep,
        rhs=[1.0] * lim_cam * numedge_sep)

    #Restrição 7
    #Deve haver pelo uma s para cada par de arestas
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
    u = [cpx.variables.add(obj=[0] * nvert,
                             lb=[0] *nvert, ub=[nvert-1] * nvert,
                             names=['u_%d_%d' % (k,i)  for i in range(nvert)]) for k in range(1,lim_cam+1)]
    #Restrição 10
    #Criação das arestas direcionadas
    cpx.linear_constraints.add(

        lin_expr = [cplex.SparsePair([a[k][i+2*nvert]] + [a[k][i+2*nvert+nedge]] + [x[k][i]], [1,1,-1])
        for k in range(lim_cam)  for i in range(nedge) ],
        senses = ['E']*nedge*lim_cam,
        rhs=[0]*nedge*lim_cam)

    #Restrição 11
    #Se usa aresta, visita o vértice
    cpx.linear_constraints.add(
        lin_expr = [cplex.SparsePair([a[k][id_edge[i][j]+2*nvert+nedge]for j in range(i,len(grafo[i])) if id_edge[i][j] != -1] + [a[k][id_edge[j][i]+2*nvert] for j in range(i) if id_edge[j][i] != -1] + [u[k][i]], [1]*nedgesout_per_vert[i] + [1]*nedgesin_per_vert[i] + [-1])
        for k in range(lim_cam)  for i in range(nvert)],
        senses = ['L']*nvert*lim_cam,
        rhs=[0]*nvert*lim_cam)
    
    #Restrição 12
    #Da os limites da numeração do vértice
    cpx.linear_constraints.add(
        lin_expr = [cplex.SparsePair([u[k][i]]+ [p[k]] + [a[k][i]] , [1,-(nvert-1),nvert-1])
        for k in range(lim_cam) for i in range(nvert)],
        senses = ['L']*lim_cam*nvert,
        rhs=[0]*lim_cam*nvert)
    
    #Restrição 13
    # Número que entra é igual ao número que sai
    cpx.linear_constraints.add(
       lin_expr = [cplex.SparsePair([a[k][i]]+[a[k][id_edge[i][j]+2*nvert+nedge]for j in range(i,len(id_edge[i])) if id_edge[i][j] != -1] + [a[k][id_edge[j][i]+2*nvert] for j in range(i) if id_edge[j][i] != -1] + [a[k][id_edge[i][j]+2*nvert] for j in range(i,len(id_edge[i])) if id_edge[i][j] != -1] + [a[k][id_edge[j][i]+2*nvert+nedge] for j in range(i) if id_edge[j][i] != -1]+ [a[k][i+nvert]], [1] + [1]*(nedgesout_per_vert[i]+nedgesin_per_vert[i])+ [-1]*(nedgesout_per_vert[i]+nedgesin_per_vert[i])+ [-1])
       for k in range(lim_cam) for i in range(nvert) ],
       senses = ['E']*lim_cam*nvert,
       rhs=[0]*lim_cam*nvert)
    
    #Restrição 14
    #Só pode entrar 1 vez no vértice por caminho: Evita ciclos
    cpx.linear_constraints.add(

       lin_expr = [cplex.SparsePair([a[k][i]]+[a[k][id_edge[i][j]+2*nvert+nedge]for j in range(i,len(grafo[i])) if id_edge[i][j] != -1] + [a[k][id_edge[j][i]+2*nvert] for j in range(i) if id_edge[j][i] != -1]+ [p[k]],[1]+ [1]*nedgesout_per_vert[i] + [1]*nedgesin_per_vert[i] + [-1])
       for k in range(lim_cam) for i in range(nvert)],
       senses = ['L']*lim_cam*nvert,
       rhs=[0]*lim_cam*nvert)
    
    #Restrição 15 e 16 Só pode haver 1 começo e 1 final
    cpx.linear_constraints.add(

       lin_expr = [cplex.SparsePair([a[k][i] for i in range(nvert)]+[p[k]], [1]*nvert+[-1])
       for k in range(lim_cam)],
       senses = ['E']*lim_cam,
       rhs=[0]*lim_cam)
    cpx.linear_constraints.add(

       lin_expr = [cplex.SparsePair([a[k][i+nvert] for i in range(nvert)]+[p[k]], [1]*nvert+[-1])
       for k in range(lim_cam)],
       senses = ['E']*lim_cam,
       rhs=[0]*lim_cam)
    
    #Restrição 17
    #Dá a numeração de um vértice subsequente, dado que está sendo visitado, tomando como consideração a numeração do vértice anterior
    cpx.linear_constraints.add(

       lin_expr = [cplex.SparsePair([u[k][i]] + [u[k][j]] + [p[k]]+ [a[k][2*nvert +id_edge[i][j]]]+ [a[k][2*nvert+nedge+id_edge[i][j]]], [-1]+[1]+[1-nvert]+[nvert-2 if j>i else nvert]+[nvert if j>i else nvert-2])
       for k in range(lim_cam) for i in range(nvert) for j in range(nvert) if id_edge[i][j] != -1],
       senses = ['L']*lim_cam*nedge*2,
       rhs=[0]*lim_cam*nedge*2)
    

    #Quero minimizar
    cpx.objective.set_sense(cpx.objective.sense.minimize)
    #Quero usar só 1 thread
    cpx.parameters.threads.set(1)
    #clock type for computation time
    cpx.parameters.clocktype.set(1) #1 - CPU TIME; 2 - Wall clock
    #time limit in seconds
    cpx.parameters.timelimit.set(3600)



    cpx.write('model.lp')  # Escreve o modelo em um arquivo LP

    starttime = cpx.get_time()

    cpx.solve()

    endtime = cpx.get_time()
    variable_names = cpx.variables.get_names()
    variable_values = cpx.solution.get_values()
    ver_var = []
    for var_name, var_value in zip(variable_names, variable_values):
        if var_value >= 0.9:
            ver_var+=[f"{var_name} = {var_value}"]
    with open(r'solucao.txt' , 'w') as f:
        for i in ver_var:
            f.write(i+'\n')

    best_integer =  cpx.solution.get_objective_value()
    best_bound = cpx.solution.MIP.get_best_objective()
    elapsed_time =-(starttime - endtime)
    resultados = f"{tipo_grafo}_{nvert}_{nedge}" + "," + f"{nvert}" + "," + f"{best_integer}"+"," + f"{best_bound}"+"," + f"{elapsed_time}"
    with open("dados.txt", "a") as file:
        file.write(resultados+ "\n")
