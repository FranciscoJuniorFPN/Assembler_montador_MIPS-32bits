#### BUSCANDO OPCODES E REGISTRADORES DO AQUIVOS DE TXT E SALVANDO EM VETORES ##########
opecodeR = []

with open("opecodeR.txt") as r:
    for linha in r:
        opecodeR += [linha.split()]

funct = []

with open("funct.txt") as f:
    for linha in f:
        funct += [linha.split()]


opecodeI = []

with open("opecodeI.txt") as i:
    for linha in i:
        opecodeI += [linha.split()]

opecodeJ = []

with open("opecodeJ.txt") as j:
    for linha in j:
        opecodeJ += [linha.split()]

registr = []

with open("registradores.txt") as rg:
    for linha in rg:
        registr += [linha.split()]


#### ABRINDO ARQUIVOS DE TESTOS DE ENTRADA E SAIDA ###################################
code     = open("code.txt", "r")
binSaida = open('binSaida.txt', 'w')


aux = []
codigo = [] # VARIAVEL ONDE SERA MANIPULADO O CODIGO DE ENTRADA E CONVERTIDO PARA BINARIO

##### FUNÇOES ########################################################################

# CONVERTE UM INTEIRO PARA BIN DE 26bits
def endereco (valor):
    valor = bin(valor)
    valor = valor[2:]
    for i in range(26-len(valor)):
        valor = "0"+valor
    return valor

# CONVERTE UM INTEIRO PARA BIN DE 16bits
def binario (valor):
    valor = bin(valor)
    valor = valor[2:]
    for i in range(16-len(valor)):
        valor = "0"+valor
    return [valor]

# BUSCA UMA STRING NO VETOR DE OPECODES DO TIPO (R)
# E RETORNO A O BINARIO CORESPONDENTE
def buscaR (valor):
    for i in opecodeR:
        if i[0] == valor.lower():
            return [i[1]]
    return ["false"]

# BUSCA UMA STRING NO VETOR DE OPECODES DO TIPO (I)
# E RETORNO A O BINARIO CORESPONDENTE
def buscaI (valor):
    for i in opecodeI:
        if i[0] == valor.lower():
            return [i[1]]
    return ["false"]

# BUSCA UMA STRING NO VETOR DE OPECODES DO TIPO (J)
# E RETORNO A O BINARIO CORESPONDENTE
def buscaJ (valor):
    for i in opecodeJ:
        if i[0] == valor.lower():
            return [i[1]]
    return ["false"]

# BUSCA UMA STRING NO VETOR DE FUNCTIONS DO TIPO (R)
# E RETORNO A O BINARIO CORESPONDENTE
def buscaRg(valor):
    for i in registr:
        if i[0] == valor:
            return [i[1]]
    return ["false"]




#### TRATANDO STRING DE ENTRADA (elimindando comentarios) ########################################
a = ';'
for linha in code:
    print(linha)
    aux = linha.replace(',', ' ').replace(':', ' : ').replace(';',' ; ').split()
    for i in range(len(aux)):
        if aux[i] == a:           
            aux = aux[:i]
            break
    codigo += [aux]

print("\n\nTrantamento da string de entrada \n", codigo)


#### ELIMINA LINHAS VAZIAS ########################################################################
aux = []
for linha in codigo:
    if linha != []:
        aux += [linha]
codigo = aux

print("\n\nEliminando linhas vazias \n", codigo)


#### GUARDA O ENDEREÇO E A STRING DO SALTO DE MEMORIA NO VETOR 'jmp' ##############################
b = ':'
jmp = []
aux = []
for i in range(len(codigo)):
    if codigo[i][1] == b:  
        jmp += [[codigo[i][0],endereco(i-len(jmp))]]

    else:
        aux += [codigo[i]]
codigo = aux

print("\n\nGuarando endereço e a string \n", codigo, "\n jmp = ", jmp)




#### CONVERTENDO DE CODE PRA BIN ########################################################
for linha in codigo:
    aux = []

    # PARA INSTRUÇOES DO TIPO (R)
    if ["false"] != buscaR(linha[0]):
        aux += buscaR(linha[0])
        if aux == ["000000"]:
            aux += buscaRg(linha[3])
            aux += buscaRg(linha[1])
            aux += buscaRg(linha[2]) 
            aux += ["00000"]
            for i in funct:
                if i[0] == linha[0].lower():
                    aux += [i[1]]
                    break
        else:
            aux += buscaRg(linha[2])
            aux += buscaRg(linha[1])
            aux += binario(int(linha[3]))


    # PARA INSTRUÇOES DO TIPO (I)
    elif ["false"] != buscaI(linha[0]):
        aux += buscaI(linha[0])
        aux += buscaRg(linha[2])
        aux += buscaRg(linha[1])
        for i in jmp:
            if i[0] == linha[3].lower():
                aux += [i[1][10:]]
                break

        
    # PARA INSTRUÇOES DO TIPO (J)
    elif ["false"] != buscaJ(linha[0]):
        aux += buscaJ(linha[0])
        for i in jmp:
            if i[0] == linha[1].lower():
                aux += [i[1]]
                break


    # ESCREVE O BINARIO RESULTANTE NO AQUIVO DE TXT
    for i in range(len(aux)):
        binSaida.write(aux[i]+" ")

    binSaida.write('\n')

    print("\n\n Convertendo pra Binario \n", aux)
