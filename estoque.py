from itens import item_existe
from utils import (
    ler_texto, ler_float, ler_opcao, data_hoje, formatar_data, cabecalho
)

def obter_saldo(estoque, codigo):
    return estoque.get(codigo, 0.0)

def registrar_movimentacao(estoque, movimentos, codigo, tipo,
                           quantidade, documento):
    saldo_atual = obter_saldo(estoque, codigo)

    if tipo == "ENTRADA":
        variacao = quantidade
    elif tipo == "SAIDA":
        variacao = -quantidade
    elif tipo == "AJUSTE":
        variacao = quantidade 
    else:
        print("Tipo de movimentacao invalido.")
        return False

    novo_saldo = round(saldo_atual + variacao, 4)

    if novo_saldo < 0:
        print(f"ERRO: saldo insuficiente (saldo atual: {saldo_atual:g}). "
              "Operacao cancelada.")
        return False

    estoque[codigo] = novo_saldo
    movimentos.append({
        "data": data_hoje(),
        "codigo": codigo,
        "tipo": tipo,
        "quantidade": variacao,
        "saldo": novo_saldo,
        "documento": documento,
    })
    return True

def verificar_alerta(itens, estoque, codigo):
    saldo = obter_saldo(estoque, codigo)
    seguranca = itens[codigo]["estoque_seguranca"]
    unidade = itens[codigo]["unidade"]
    if saldo < seguranca:
        print(f"ALERTA: saldo ({saldo:g} {unidade}) abaixo do estoque de "
              f"seguranca ({seguranca} {unidade}).")


def obter_kardex(movimentos, codigo):
    return [mov for mov in movimentos if mov["codigo"] == codigo]


def exibir_kardex(itens, estoque, movimentos, codigo):
    if not item_existe(itens, codigo):
        print("Item nao encontrado.")
        return

    item = itens[codigo]
    cabecalho(f"KARDEX - {codigo} {item['descricao']} ({item['unidade']})")
    print(f"{'Data':<12}{'Tipo':<9}{'Qtde':>8}{'Saldo':>9}  Documento")

    kardex = obter_kardex(movimentos, codigo)
    if not kardex:
        print("Nenhuma movimentacao registrada.")
    for mov in kardex:
        print(f"{formatar_data(mov['data']):<12}{mov['tipo']:<9}"
              f"{mov['quantidade']:>+8g}{mov['saldo']:>9g}  "
              f"{mov['documento']}")

    verificar_alerta(itens, estoque, codigo)


def movimentar_estoque(itens, estoque, movimentos):
    while True:
        codigo = ler_texto("Codigo do item (0 para voltar): ").upper()
        if codigo == "0":
            return
        if not item_existe(itens, codigo):
            print("Item nao encontrado.")
            continue
        break

    tipo_letra = ler_opcao("Tipo [E]ntrada [S]aida [A]juste: ",
                           ["E", "S", "A"])

    if tipo_letra == "E":
        tipo = "ENTRADA"
        quantidade = ler_float("Quantidade: ", 0.01)
    elif tipo_letra == "S":
        tipo = "SAIDA"
        quantidade = ler_float("Quantidade: ", 0.01)
    else:
        tipo = "AJUSTE"
        while True:
            quantidade = ler_float("Quantidade do ajuste "
                                   "(use - para diminuir): ")
            if quantidade == 0:
                print("O ajuste nao pode ser zero.")
                continue
            break

    documento = ler_texto("Documento/motivo: ")

    if registrar_movimentacao(estoque, movimentos, codigo, tipo,
                              quantidade, documento):
        print(f"Movimentacao registrada. Saldo atual: "
              f"{obter_saldo(estoque, codigo):g}")
        verificar_alerta(itens, estoque, codigo)


def listar_posicao_estoque(itens, estoque):
    cabecalho("POSICAO DE ESTOQUE")
    print(f"{'Codigo':<8}{'Descricao':<28}{'Saldo':>9}{'Seguranca':>11}")
    for codigo, dados in itens.items():
        saldo = obter_saldo(estoque, codigo)
        marca = "  <- ABAIXO" if saldo < dados["estoque_seguranca"] else ""
        print(f"{codigo:<8}{dados['descricao']:<28}{saldo:>9g}"
              f"{dados['estoque_seguranca']:>11}{marca}")