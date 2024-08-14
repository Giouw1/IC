import pandas as pd

def cria_tabela(arquivo,tabela_feita,output):
    try:
        table = pd.read_csv(open(tabela_feita))
    except pd.errors.EmptyDataError:
        data = {"Nome": [],
            "Nos": [],
            "Best Integer": [],
            "Best bound": [],
            "Elapsed Time": [],
        }
    else:
        table = pd.read_csv(open(tabela_feita))
        data = table.to_dict(orient = "list")


    for line in arquivo:
        marcador = 1
        for element in range(len(line)):
            if (line[element] == ",") and (marcador == 1):
                data["Nome"] += [str(line[0:element])]
                endereço = element
                marcador = 2
            elif (line[element] == ",") and (marcador == 2):
                data["Nos"] += [int(line[endereço+1:element])]
                endereço = element
                marcador = 3
            elif (line[element] == ",") and (marcador == 3):
                data["Best Integer"] += [float(line[endereço+1:element])]
                endereço = element
                marcador = 4
            elif (line[element] == ",") and (marcador == 4):
                data["Best bound"] += [float(line[endereço+1:element])]
                endereço = element
                marcador = 5
            elif (marcador == 5):
                data["Elapsed Time"] += [float(line[endereço+1:])]
                break
    result = pd.DataFrame.from_dict(data)
    result.to_csv(open(output,"w"), index=False)


#A lógica vai ser a seguinte: vou acessar um endereço com uma tabela já criada (se o endereço for vazio, cria a tabela
#e já adiciona as primeiras colunas, vou percorrer os dados.txt, adiciona-lo à tabela, e apagar o dados.txt)

