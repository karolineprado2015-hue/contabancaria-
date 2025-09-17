import datetime
from typing import List, Optional


class ContaBancaria:
    def __init__(self, numero_conta: str, titular: str, saldo_inicial: float = 0.0):
        self.numero_conta = numero_conta
        self.titular = titular
        self.saldo = saldo_inicial
        self.historico: List[dict] = []
        self.data_criacao = datetime.datetime.now()

        # Adiciona transação inicial se houver saldo
        if saldo_inicial > 0:
            self._adicionar_transacao("Depósito Inicial", saldo_inicial)

    def depositar(self, valor: float) -> bool:
        """Realiza um depósito na conta"""
        if valor <= 0:
            print("❌ Valor de depósito deve ser positivo!")
            return False

        self.saldo += valor
        self._adicionar_transacao("Depósito", valor)
        print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True

    def sacar(self, valor: float) -> bool:
        """Realiza um saque da conta"""
        if valor <= 0:
            print("❌ Valor de saque deve ser positivo!")
            return False

        if valor > self.saldo:
            print("❌ Saldo insuficiente!")
            return False

        self.saldo -= valor
        self._adicionar_transacao("Saque", -valor)
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        return True

    def transferir(self, conta_destino: 'ContaBancaria', valor: float) -> bool:
        """Realiza uma transferência para outra conta"""
        if valor <= 0:
            print("❌ Valor de transferência deve ser positivo!")
            return False

        if valor > self.saldo:
            print("❌ Saldo insuficiente para transferência!")
            return False

        # Realiza a transferência
        self.saldo -= valor
        conta_destino.saldo += valor

        # Registra no histórico das duas contas
        self._adicionar_transacao(f"Transferência para {conta_destino.numero_conta}", -valor)
        conta_destino._adicionar_transacao(f"Transferência de {self.numero_conta}", valor)

        print(f"✅ Transferência de R$ {valor:.2f} para conta {conta_destino.numero_conta} realizada com sucesso!")
        return True

    def consultar_saldo(self) -> float:
        """Consulta o saldo atual da conta"""
        print(f"💰 Saldo atual: R$ {self.saldo:.2f}")
        return self.saldo

    def _adicionar_transacao(self, tipo: str, valor: float):
        """Adiciona uma transação ao histórico (método privado)"""
        transacao = {
            'data': datetime.datetime.now(),
            'tipo': tipo,
            'valor': valor,
            'saldo_apos': self.saldo
        }
        self.historico.append(transacao)

    def extrato(self, limite: int = 10) -> None:
        """Exibe o extrato das últimas transações"""
        print(f"\n📋 EXTRATO - Conta: {self.numero_conta}")
        print(f"Titular: {self.titular}")
        print(f"Saldo Atual: R$ {self.saldo:.2f}")
        print("-" * 50)

        if not self.historico:
            print("Nenhuma transação encontrada.")
            return

        # Exibe as últimas transações (limitadas)
        transacoes_recentes = self.historico[-limite:]

        for transacao in transacoes_recentes:
            data_formatada = transacao['data'].strftime("%d/%m/%Y %H:%M")
            valor = transacao['valor']
            sinal = "+" if valor >= 0 else ""
            print(
                f"{data_formatada} | {transacao['tipo']:<20} | {sinal}R$ {valor:>8.2f} | Saldo: R$ {transacao['saldo_apos']:.2f}")

        print("-" * 50)

    def __str__(self) -> str:
        return f"Conta: {self.numero_conta} | Titular: {self.titular} | Saldo: R$ {self.saldo:.2f}"


class Banco:
    def __init__(self, nome: str):
        self.nome = nome
        self.contas: dict[str, ContaBancaria] = {}

    def criar_conta(self, numero_conta: str, titular: str, saldo_inicial: float = 0.0) -> Optional[ContaBancaria]:
        """Cria uma nova conta bancária"""
        if numero_conta in self.contas:
            print(f"❌ Conta {numero_conta} já existe!")
            return None

        nova_conta = ContaBancaria(numero_conta, titular, saldo_inicial)
        self.contas[numero_conta] = nova_conta
        print(f"✅ Conta {numero_conta} criada com sucesso para {titular}!")
        return nova_conta

    def buscar_conta(self, numero_conta: str) -> Optional[ContaBancaria]:
        """Busca uma conta pelo número"""
        return self.contas.get(numero_conta)

    def listar_contas(self) -> None:
        """Lista todas as contas do banco"""
        print(f"\n🏦 CONTAS DO {self.nome.upper()}")
        print("-" * 60)

        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return

        for conta in self.contas.values():
            print(conta)


def limpar_tela():
    """Limpa a tela (simulado com quebras de linha)"""
    print("\n" * 3)


def pausar():
    """Pausa a execução até o usuário pressionar Enter"""
    input("\n⏸️  Pressione Enter para continuar...")


def obter_numero_float(mensagem: str) -> float:
    """Obtém um número float válido do usuário"""
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("❌ Por favor, digite um número válido!")


def menu_principal():
    """Exibe o menu principal"""
    print("\n" + "=" * 50)
    print("🏦 SISTEMA BANCÁRIO DA KAROL")
    print("=" * 50)
    print("1. 🆕 Criar nova conta")
    print("2. 💰 Depositar")
    print("3. 💸 Sacar")
    print("4. 🔄 Transferir")
    print("5. 📊 Consultar saldo")
    print("6. 📋 Ver extrato")
    print("7. 📝 Listar todas as contas")
    print("0. 🚪 Sair")
    print("-" * 50)


def criar_conta_interativa(banco: Banco):
    """Cria uma conta de forma interativa"""
    print("\n🆕 CRIAR NOVA CONTA")
    print("-" * 30)

    numero_conta = input("📋 Digite o número da conta: ").strip()
    if not numero_conta:
        print("❌ Número da conta não pode estar vazio!")
        return

    titular = input("👤 Digite o nome do titular: ").strip()
    if not titular:
        print("❌ Nome do titular não pode estar vazio!")
        return

    saldo_inicial = obter_numero_float("💰 Digite o saldo inicial (ou 0): R$ ")
    if saldo_inicial < 0:
        print("❌ Saldo inicial não pode ser negativo!")
        return

    banco.criar_conta(numero_conta, titular, saldo_inicial)


def operacao_deposito(banco: Banco):
    """Realiza depósito de forma interativa"""
    print("\n💰 DEPÓSITO")
    print("-" * 20)

    numero_conta = input("📋 Digite o número da conta: ").strip()
    conta = banco.buscar_conta(numero_conta)

    if not conta:
        print("❌ Conta não encontrada!")
        return

    print(f"👤 Titular: {conta.titular}")
    print(f"💰 Saldo atual: R$ {conta.saldo:.2f}")

    valor = obter_numero_float("💰 Digite o valor do depósito: R$ ")
    conta.depositar(valor)


def operacao_saque(banco: Banco):
    """Realiza saque de forma interativa"""
    print("\n💸 SAQUE")
    print("-" * 15)

    numero_conta = input("📋 Digite o número da conta: ").strip()
    conta = banco.buscar_conta(numero_conta)

    if not conta:
        print("❌ Conta não encontrada!")
        return

    print(f"👤 Titular: {conta.titular}")
    print(f"💰 Saldo atual: R$ {conta.saldo:.2f}")

    valor = obter_numero_float("💸 Digite o valor do saque: R$ ")
    conta.sacar(valor)


def operacao_transferencia(banco: Banco):
    """Realiza transferência de forma interativa"""
    print("\n🔄 TRANSFERÊNCIA")
    print("-" * 25)

    numero_origem = input("📋 Digite o número da conta de origem: ").strip()
    conta_origem = banco.buscar_conta(numero_origem)

    if not conta_origem:
        print("❌ Conta de origem não encontrada!")
        return

    print(f"👤 Titular origem: {conta_origem.titular}")
    print(f"💰 Saldo atual: R$ {conta_origem.saldo:.2f}")

    numero_destino = input("📋 Digite o número da conta de destino: ").strip()
    conta_destino = banco.buscar_conta(numero_destino)

    if not conta_destino:
        print("❌ Conta de destino não encontrada!")
        return

    print(f"👤 Titular destino: {conta_destino.titular}")

    valor = obter_numero_float("💰 Digite o valor da transferência: R$ ")
    conta_origem.transferir(conta_destino, valor)


def consultar_saldo_interativo(banco: Banco):
    """Consulta saldo de forma interativa"""
    print("\n📊 CONSULTAR SALDO")
    print("-" * 25)

    numero_conta = input("📋 Digite o número da conta: ").strip()
    conta = banco.buscar_conta(numero_conta)

    if not conta:
        print("❌ Conta não encontrada!")
        return

    print(f"👤 Titular: {conta.titular}")
    conta.consultar_saldo()


def ver_extrato_interativo(banco: Banco):
    """Mostra extrato de forma interativa"""
    print("\n📋 EXTRATO")
    print("-" * 15)

    numero_conta = input("📋 Digite o número da conta: ").strip()
    conta = banco.buscar_conta(numero_conta)

    if not conta:
        print("❌ Conta não encontrada!")
        return

    try:
        limite = int(input("📊 Quantas transações mostrar? (padrão 10): ") or "10")
    except ValueError:
        limite = 10

    conta.extrato(limite)


def main():
    # Criar o banco
    banco = Banco("Banco Digital")

    # Criar algumas contas iniciais para demonstração
    banco.criar_conta("1001", "João Silva", 1500.0)
    banco.criar_conta("1002", "Maria Santos", 800.0)

    print("🎉 Banco iniciado com 2 contas de demonstração:")
    print("   - Conta 1001: João Silva (R$ 1500,00)")
    print("   - Conta 1002: Maria Santos (R$ 800,00)")

    while True:
        menu_principal()

        try:
            opcao = input("🎯 Escolha uma opção: ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 Saindo do sistema...")
            break

        if opcao == "1":
            criar_conta_interativa(banco)
            pausar()

        elif opcao == "2":
            operacao_deposito(banco)
            pausar()

        elif opcao == "3":
            operacao_saque(banco)
            pausar()

        elif opcao == "4":
            operacao_transferencia(banco)
            pausar()

        elif opcao == "5":
            consultar_saldo_interativo(banco)
            pausar()

        elif opcao == "6":
            ver_extrato_interativo(banco)
            pausar()

        elif opcao == "7":
            banco.listar_contas()
            pausar()

        elif opcao == "0":
            print("\n👋 Obrigado por usar o Banco Digital!")
            print("💙 Tenha um ótimo dia!")
            break

        else:
            print("❌ Opção inválida! Tente novamente.")
            pausar()


if __name__ == "__main__":
    main ()