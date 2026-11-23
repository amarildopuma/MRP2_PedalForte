from utils import cabecalho, ler_opcao, ler_texto
from persistencia import carregar_tudo, salvar_tudo
from itens import cadastrar_item, listar_itens, alterar_item
from estrutura import cadastrar_componente, exibir_bom
from estoque import (
    movimentar_estoque, exibir_kardex, listar_posicao_estoque
)
from mps import cadastrar_mps, alterar_mps, exibir_mps
from mrp import executar_mrp, exibir_registro_mrp
from ordens import listar_ordens, firmar_ordem, liberar_ordem, encerrar_ordem


# Todos os dados do sistema ficam num dicionario so, para passar de um
# submenu para outro sem repetir seis parametros em cada funcao.
#   dados = {"itens", "estrutura", "estoque", "mps", "ordens",
#            "movimentos", "registros"}
# "registros" e o resultado do ultimo MRP (so existe em memoria).


def mostrar_opcoes(titulo, opcoes):
    """Imprime o submenu e devolve a opcao escolhida (texto)."""
    cabecalho(titulo)
    for numero, descricao in opcoes:
        print(f"  {numero} - {descricao}")
    validas = [numero for numero, _ in opcoes]
    return ler_opcao("Escolha: ", validas)


def salvar(dados):
    salvar_tudo(dados["itens"], dados["estrutura"], dados["estoque"],
                dados["mps"], dados["ordens"], dados["movimentos"])


def menu_itens(dados):
    while True:
        opcao = mostrar_opcoes("ITENS", [
            ("1", "Cadastrar item"),
            ("2", "Listar itens"),
            ("3", "Alterar item"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            cadastrar_item(dados["itens"])
        elif opcao == "2":
            listar_itens(dados["itens"])
        elif opcao == "3":
            alterar_item(dados["itens"])
        else:
            return
        salvar(dados)


def menu_estrutura(dados):
    while True:
        opcao = mostrar_opcoes("ESTRUTURA DE PRODUTO (BOM)", [
            ("1", "Cadastrar componente"),
            ("2", "Exibir BOM de um item"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            cadastrar_componente(dados["estrutura"], dados["itens"])
        elif opcao == "2":
            codigo = ler_texto("Codigo do item: ").upper()
            exibir_bom(dados["itens"], dados["estrutura"], codigo)
        else:
            return
        salvar(dados)


def menu_estoque(dados):
    while True:
        opcao = mostrar_opcoes("ESTOQUE", [
            ("1", "Movimentar estoque (entrada/saida/ajuste)"),
            ("2", "Kardex de um item"),
            ("3", "Posicao de estoque"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            movimentar_estoque(dados["itens"], dados["estoque"],
                               dados["movimentos"])
        elif opcao == "2":
            codigo = ler_texto("Codigo do item: ").upper()
            exibir_kardex(dados["itens"], dados["estoque"],
                          dados["movimentos"], codigo)
        elif opcao == "3":
            listar_posicao_estoque(dados["itens"], dados["estoque"])
        else:
            return
        salvar(dados)


def menu_mps(dados):
    while True:
        opcao = mostrar_opcoes("PLANO MESTRE DE PRODUCAO (MPS)", [
            ("1", "Cadastrar MPS"),
            ("2", "Alterar semana do MPS"),
            ("3", "Exibir MPS"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            cadastrar_mps(dados["itens"], dados["mps"])
        elif opcao == "2":
            alterar_mps(dados["itens"], dados["mps"])
        elif opcao == "3":
            exibir_mps(dados["itens"], dados["mps"])
        else:
            return
        salvar(dados)


def menu_mrp(dados):
    while True:
        opcao = mostrar_opcoes("MRP", [
            ("1", "Executar MRP"),
            ("2", "Ver registro MRP de um item"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            dados["registros"] = executar_mrp(
                dados["itens"], dados["estrutura"], dados["estoque"],
                dados["mps"], dados["ordens"])
        elif opcao == "2":
            codigo = ler_texto("Codigo do item: ").upper()
            exibir_registro_mrp(dados["itens"], dados["registros"], codigo)
        else:
            return
        salvar(dados)


def pedir_ordem_e_executar(dados, acao):
    numero = ler_texto("Numero da ordem (ex: OP-0001): ").upper()
    acao(dados["ordens"], numero)


def menu_ordens(dados):
    while True:
        opcao = mostrar_opcoes("ORDENS", [
            ("1", "Listar ordens"),
            ("2", "Firmar ordem"),
            ("3", "Liberar ordem"),
            ("4", "Encerrar ordem"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            listar_ordens(dados["ordens"])
        elif opcao == "2":
            pedir_ordem_e_executar(dados, firmar_ordem)
        elif opcao == "3":
            pedir_ordem_e_executar(dados, liberar_ordem)
        elif opcao == "4":
            pedir_ordem_e_executar(dados, encerrar_ordem)
        else:
            return
        salvar(dados)


def menu_principal():
    itens, estrutura, estoque, mps, ordens, movimentos = carregar_tudo()
    dados = {
        "itens": itens,
        "estrutura": estrutura,
        "estoque": estoque,
        "mps": mps,
        "ordens": ordens,
        "movimentos": movimentos,
        "registros": {},
    }

    while True:
        opcao = mostrar_opcoes("MRP II - PEDAL FORTE BICICLETAS", [
            ("1", "Itens"),
            ("2", "Estrutura de produto (BOM)"),
            ("3", "Estoque"),
            ("4", "MPS"),
            ("5", "MRP"),
            ("6", "Ordens"),
            ("0", "Sair"),
        ])
        if opcao == "1":
            menu_itens(dados)
        elif opcao == "2":
            menu_estrutura(dados)
        elif opcao == "3":
            menu_estoque(dados)
        elif opcao == "4":
            menu_mps(dados)
        elif opcao == "5":
            menu_mrp(dados)
        elif opcao == "6":
            menu_ordens(dados)
        else:
            salvar(dados)
            print("Dados salvos. Ate logo!")
            return