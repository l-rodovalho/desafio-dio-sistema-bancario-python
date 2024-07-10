from abc import ABC, abstractmethod
from datetime import datetime
import textwrap


class Cliente:
    
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adiconar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nasc, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nasc = data_nasc
        self.cpf = cpf


class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        
        saldo = self.saldo
        
        if valor > saldo:
            print('Erro! Saldo insuficiente!')
        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True
        else:
            print('Erro! Valor inválido!')
            
        return False
        
    def depositar(self, valor):
        
        if valor > 0:
            self._saldo += valor
            print('Depósito realizado com sucesso!')
        else:
            print('Erro! Valor inválido!')
            return False
        
        return True

    
class ContaCorrente(Conta):
    
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if valor > self.limite:
            print('Erro! Limite insufuciente!')
        elif numero_saques >= self.limite_saques:
            print('Erro! Limite de saques excedido!')
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência: {self.agencia}
            Conta: {self.numero}
            Titular: {self.cliente.nome}
        """
    

class Historico:
    
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({"tipo": transacao.__class__.__name__, "valor": transacao.valor, "data": datetime.now().strftime('%d-%m-%Y %H:%M')})


class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(sel, conta):
        pass


class Saque(Transacao):
    
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def filtrar_cliente(cpf, clientes):
    
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]

    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):

    if not cliente.contas:
        print ('Cliente não possui conta!')
        return
    
    return cliente.contas[0]


def depositar(clientes):

    cpf = input("Digite o CPF do cliente (apenas números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')

    valor = float(input('Digite o valor do depósito: '))

    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):

    cpf = input("Digite o CPF do cliente (apenas números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')

    valor = float(input('Digite o valor do saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):

    cpf = input("Digite o CPF do cliente (apenas números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n---------------Extrato---------------")
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Nenhuma movimentação realizada."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: R${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: R${conta.saldo:.2f}")
    print('-------------------------------------')


def criar_cliente(clientes):

    cpf = input("Digite o CPF do cliente (apenas números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('O cliente com CPF informado já está cadastrado!')
        return
    
    nome = input('Digite o nome completo: ')
    data_nasc = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Digite o endereço (lougradouro, número - bairro - cidade/UF): ')

    cliente = PessoaFisica(nome=nome, data_nasc=data_nasc, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('Cliente cadastrado com sucesso!')


def criar_conta(numero_conta, clientes, contas):

    cpf = input("Digite o CPF do cliente (apenas números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado! Erro ao criar conta!')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('Conta criada com sucesso!')


def listar_contas(contas):

    for conta in contas:
        print('-' * 37)
        print(textwrap.dedent(str(conta)))


menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[c] Cadastrar cliente
[a] Criar conta
[l] Listar contas
[q] Sair

=> """

clientes = []
contas = []

while True:

    opcao = input(menu)

    if opcao == "d":
        depositar(clientes)

    elif opcao == "s":
        sacar(clientes)

    elif opcao == "e":
        exibir_extrato(clientes)

    elif opcao == "c":
        criar_cliente(clientes)

    elif opcao == "a":
        numero_conta = len(contas) + 1
        criar_conta(numero_conta, clientes, contas)

    elif opcao == "l":
        listar_contas(contas)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
