def depositar(saldo, extrato):  # acrescenta valor do depósito ao saldo e adiciona operação ao extrato

    valor = float(input("Informe o valor do depósito desejado: "))

    if valor > 0:

        saldo += valor

        extrato += f"Depósito de R$ {valor:.2f}\n"

        print(f"Depósito de R$ {valor:.2f} realizado! Novo saldo: R$ {saldo:.2f}")

    else:
        print("Operação inválida!")

    return saldo, extrato


def sacar(*, saldo, extrato, numero_saques):  # retira valor do saldo e adiciona operação ao extrato

    if saldo > 0:

        if numero_saques < 3:  # 3 é o número máximo de saques diários
            valor = float(input(f"Informe o valor do saque desejado - Saldo: R$ {saldo:.2f} - Limite: R$ 500.00 : "))

            if valor > 0 and valor <= 500:  # 500 é o valor máximo de um saque

                if valor > saldo:
                    print("Saldo insuficiente!")

                else:

                    numero_saques += 1

                    saldo -= valor

                    extrato += f"Saque de R$ {valor:.2f}\n"

                    print(f"Saque de R$ {valor:.2f} realizado! Novo saldo: R$ {saldo:.2f}")

            else:
                print("Valor limite de saque excedido!")

        else:
            print("Número máximo de saques diário atingido!")

    else:
        print("Saldo insuficiente!")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, *, extrato):

    extrato += f"Saldo após operações: {saldo:.2f}\n-----------------------------------------------\n"

    print(extrato)


def criar_usuario(usuarios):  # armazena os dados do cliente em um dicionário, e é adicionado a lista usuários

    nome = input("Nome: ")

    nascimento = input("Data de nascimento (dd/mm/aaaa): ")

    cpf = input("Digite o CPF (apenas números): ")

    for usuario in usuarios:
        if usuario["cpf"] == cpf:  # cpf deve ser único

            print("CPF já cadastrado!")

            return usuarios

    endereco = input("Endereço (logradouro, número - bairro - cidade/UF): ")

    usuarios.append({"nome": nome, "nascimento": nascimento, "cpf": cpf, "endereco": endereco})

    print("Cliente cadastrado com sucesso!")

    return usuarios


def criar_conta(contas, usuarios):  # contas armazenadas em um dicionário, que é adicionado a lista contas

    cpf = input("Digite o CPF do cliente (apenas números): ")

    cpf_valido = False

    for usuario in usuarios:
        if usuario["cpf"] == cpf:  # toda conta deve ser vinculada a algum cliente

            cpf_valido = True

            nome = usuario["nome"]

    if cpf_valido == False:

        print("Usuário não encontrado!")

        return contas

    numero = len(contas) + 1

    contas.append({"agencia": "0001", "numero": numero, "nome": nome, "cpf": cpf})

    print(f"Conta cadastrada com sucesso! Agência: 0001 | Número: {numero}")

    return contas


def listar_clientes(usuarios):

    for usuario in usuarios:

        print(30 * "-")
        print(f"Nome: {usuario['nome']}")
        print(f"Data de nascimento: {usuario['nascimento']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Endereco: {usuario['endereco']}")

    print(30 * "-")


def buscar_conta(contas):  # lista todas as contas do usuário (caso exista)

    cpf = input("Digite o CPF do cliente (apenas números): ")

    encontrado = False

    for conta in contas:
        if conta["cpf"] == cpf:

            encontrado = True

            print(30 * "-")
            print(f"Nome: {conta['nome']}")
            print(f"Agência: {conta['agencia']}")
            print(f"Numero: {conta['numero']}")

    if encontrado:
        print(30 * "-")

    else:
        print("Nenhuma conta encontrada para o CPF informado!")


menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[c] Cadastrar cliente
[a] Criar conta corrente
[l] Listar clientes
[b] Buscar conta
[q] Sair

=> """

saldo = 0
limite = 500
extrato = "--------------------Extrato--------------------\nSaldo inicial: R$ 0.00\n"
numero_saques = 0
usuarios = []
contas = []

while True:

    opcao = input(menu)

    if opcao == "d":
        saldo, extrato = depositar(saldo, extrato)

    elif opcao == "s":
        saldo, extrato, numero_saques = sacar(saldo=saldo, extrato=extrato, numero_saques=numero_saques)

    elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)

    elif opcao == "c":
        usuarios = criar_usuario(usuarios)

    elif opcao == "a":
        contas = criar_conta(contas, usuarios)

    elif opcao == "l":
        listar_clientes(usuarios)

    elif opcao == "b":
        buscar_conta(contas)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
