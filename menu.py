from utils import cabecalho, ler_opcao, ler_texto
from persistencia import carregar_tudo, salvar_tudo
from itens import cadastrar_item, listar_itens, alterar_item
from estrutura import cadastrar_componente, exibir_bom
from estoque import (
    movimentar_estoque, exibir_kardex, listar_posicao_estoque
)
from mps import cadastrar_mps, alterar_mps, exibir_mps
from mrp import executar_mrp, exibir_registro_mrp
from ordens import (
    listar_ordens, firmar_ordem, liberar_ordem, apontar_producao,
    receber_compra
)
from capacidade import (
    cadastrar_centro, listar_centros, cadastrar_roteiro, listar_roteiros,
    exibir_crp
)
from custos import exibir_custo_padrao
from relatorios import exportar_posicao_estoque, exportar_ordens
import graficos


# Todos os dados do sistema ficam num dicionario so, para passar de um
# submenu para outro sem repetir oito parametros em cada funcao.
#   dados = {"itens", "estrutura", "estoque", "mps", "ordens",
#            "movimentos", "centros", "roteiros", "registros"}
# "registros" e o resultado do ultimo MRP (so existe em memoria).


def mostrar_opcoes(titulo, opcoes):
    """Imprime o submenu e devolve a opcao escolhida (texto)."""
    cabecalho(titulo)
    for numero, descricao in opcoes:
        print(f"  {numero} - {descricao}")
    validas = [numero for numero, _ in opcoes]
    return ler_opcao("Escolha: ", validas)


def pedir_codigo(mensagem="Codigo do item (0 para voltar): "):
    """Pede um codigo; devolve None se a pessoa digitar 0."""
    codigo = ler_texto(mensagem).upper()
    if codigo == "0":
        return None
    return codigo


def salvar(dados):
    salvar_tudo(dados["itens"], dados["estrutura"], dados["estoque"],
                dados["mps"], dados["ordens"], dados["movimentos"],
                dados["centros"], dados["roteiros"])


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


def menu_centros(dados):
    while True:
        opcao = mostrar_opcoes("CENTROS DE TRABALHO", [
            ("1", "Cadastrar centro"),
            ("2", "Listar centros"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            cadastrar_centro(dados["centros"])
        elif opcao == "2":
            listar_centros(dados["centros"])
        else:
            return
        salvar(dados)


def menu_roteiros(dados):
    while True:
        opcao = mostrar_opcoes("ROTEIROS DE OPERACAO", [
            ("1", "Cadastrar roteiro de um item"),
            ("2", "Listar roteiros"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            cadastrar_roteiro(dados["itens"], dados["centros"],
                              dados["roteiros"])
        elif opcao == "2":
            listar_roteiros(dados["itens"], dados["centros"],
                            dados["roteiros"])
        else:
            return
        salvar(dados)


def menu_cadastros(dados):
    while True:
        opcao = mostrar_opcoes("CADASTROS", [
            ("1", "Itens"),
            ("2", "Estrutura de produto (BOM)"),
            ("3", "Centros de trabalho"),
            ("4", "Roteiros"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            menu_itens(dados)
        elif opcao == "2":
            menu_estrutura(dados)
        elif opcao == "3":
            menu_centros(dados)
        elif opcao == "4":
            menu_roteiros(dados)
        else:
            return


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


def pedir_numero_ordem():
    return ler_texto("Numero da ordem (ex: OP-0001): ").upper()


def menu_ordens(dados):
    while True:
        opcao = mostrar_opcoes("ORDENS", [
            ("1", "Listar ordens"),
            ("2", "Firmar ordem"),
            ("3", "Liberar ordem"),
            ("4", "Apontar producao (OP liberada)"),
            ("5", "Receber compra (OC liberada)"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            listar_ordens(dados["ordens"])
        elif opcao == "2":
            firmar_ordem(dados["ordens"], pedir_numero_ordem())
        elif opcao == "3":
            liberar_ordem(dados["ordens"], pedir_numero_ordem())
        elif opcao == "4":
            apontar_producao(dados["itens"], dados["estrutura"],
                             dados["estoque"], dados["movimentos"],
                             dados["ordens"], pedir_numero_ordem())
        elif opcao == "5":
            receber_compra(dados["estoque"], dados["movimentos"],
                           dados["ordens"], pedir_numero_ordem())
        else:
            return
        salvar(dados)


def menu_crp(dados):
    if not dados["centros"]:
        print("Nenhum centro cadastrado.")
        return
    listar_centros(dados["centros"])
    while True:
        codigo = pedir_codigo("Codigo do centro (0 para voltar): ")
        if codigo is None:
            return
        exibir_crp(dados["centros"], dados["roteiros"], dados["ordens"],
                   codigo)


def menu_custos(dados):
    while True:
        codigo = pedir_codigo("Codigo do PA ou SA (0 para voltar): ")
        if codigo is None:
            return
        exibir_custo_padrao(dados["itens"], dados["estrutura"],
                            dados["centros"], dados["roteiros"], codigo)


def menu_relatorios(dados):
    while True:
        opcao = mostrar_opcoes("RELATORIOS (EXPORTAR CSV)", [
            ("1", "Posicao de estoque"),
            ("2", "Lista de ordens"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            exportar_posicao_estoque(dados["itens"], dados["estoque"])
        elif opcao == "2":
            exportar_ordens(dados["ordens"])
        else:
            return


def menu_graficos(dados):
    while True:
        opcao = mostrar_opcoes("GRAFICOS DE GESTAO", [
            ("1", "Posicao de estoque (saldo x seguranca)"),
            ("2", "Estoque projetado de um item (MRP)"),
            ("3", "Ordens por semana de entrega (OP x OC)"),
            ("4", "Carga x capacidade de um centro"),
            ("0", "Voltar"),
        ])
        if opcao == "1":
            graficos.grafico_posicao_estoque(dados["itens"],
                                             dados["estoque"])
        elif opcao == "2":
            codigo = pedir_codigo()
            if codigo is not None:
                graficos.grafico_estoque_projetado(
                    dados["itens"], dados["registros"], codigo)
        elif opcao == "3":
            graficos.grafico_ordens_por_semana(dados["ordens"])
        elif opcao == "4":
            codigo = pedir_codigo("Codigo do centro (0 para voltar): ")
            if codigo is not None:
                graficos.grafico_carga_capacidade(
                    dados["centros"], dados["roteiros"], dados["ordens"],
                    codigo)
        else:
            return


def menu_principal():
    (itens, estrutura, estoque, mps, ordens, movimentos,
     centros, roteiros) = carregar_tudo()
    dados = {
        "itens": itens,
        "estrutura": estrutura,
        "estoque": estoque,
        "mps": mps,
        "ordens": ordens,
        "movimentos": movimentos,
        "centros": centros,
        "roteiros": roteiros,
        "registros": {},
    }

    while True:
        opcao = mostrar_opcoes("MRP II - PEDAL FORTE BICICLETAS", [
            ("1", "Cadastros (itens, estrutura, centros, roteiros)"),
            ("2", "Estoque (movimentar, saldo, kardex)"),
            ("3", "Plano Mestre de Producao (MPS)"),
            ("4", "Executar MRP"),
            ("5", "Ordens de producao e de compra"),
            ("6", "Carga x capacidade (CRP)"),
            ("7", "Custo padrao dos produtos"),
            ("8", "Relatorios (exportar CSV)"),
            ("9", "Graficos de gestao"),
            ("0", "Sair"),
        ])
        if opcao == "1":
            menu_cadastros(dados)
        elif opcao == "2":
            menu_estoque(dados)
        elif opcao == "3":
            menu_mps(dados)
        elif opcao == "4":
            menu_mrp(dados)
        elif opcao == "5":
            menu_ordens(dados)
        elif opcao == "6":
            menu_crp(dados)
        elif opcao == "7":
            menu_custos(dados)
        elif opcao == "8":
            menu_relatorios(dados)
        elif opcao == "9":
            menu_graficos(dados)
        else:
            salvar(dados)
            print("Dados salvos. Ate logo!")
            return
