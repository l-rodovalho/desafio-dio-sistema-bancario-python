menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = "--------------------Extrato--------------------\nSaldo inicial: R$ 0.00\n"
numero_saques = 0

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito desejado: "))

        if valor > 0:
            
            saldo += valor
            
            extrato += f"Depósito de R$ {valor:.2f}\n"
            
            print(f"Depósito de R$ {valor:.2f} realizado! Novo saldo: R$ {saldo:.2f}")
        
        else:
            print("Operação inválida!")

    elif opcao == "s":
        
        if saldo > 0:

            if numero_saques < 3:
                valor = float(input(f"Informe o valor do saque desejado - Saldo: R$ {saldo:.2f} - Limite: R$ 500.00 : "))

                if valor > 0 and valor <= 500:

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

    elif opcao == "e":
        
        extrato += f"Saldo após operações: {saldo:.2f}\n-----------------------------------------------\n"

        print(extrato)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
