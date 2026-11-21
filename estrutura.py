from itens import item_existe
from utils import tipo_do_codigo, ler_float, ler_texto


def validar_componente(itens, pai, filho):
    if not item_existe(itens, pai) or not item_existe(itens, filho):
        return False

    tipo_pai = tipo_do_codigo(pai)
    tipo_filho = tipo_do_codigo(filho)

    if tipo_pai == "PA":
        return tipo_filho in ["SA", "MP"]
    if tipo_pai == "SA":
        return tipo_filho == "MP"
    return False


def cadastrar_componente(estrutura, itens):
    pai = ler_texto("Código do pai: ").upper()
    filho = ler_texto("Código do componente: ").upper()

    if not validar_componente(itens, pai, filho):
        print("Combinação inválida.")
        return

    quantidade = ler_float("Quantidade por unidade do pai: ", 0.01)

    if pai not in estrutura:
        estrutura[pai] = {}
    estrutura[pai][filho] = quantidade
    print("Componente cadastrado.")


def listar_componentes(estrutura, pai):
    return estrutura.get(pai, {})

def explodir_bom(estrutura, codigo, nivel=0):
    resultado = []
    for filho, qtd in listar_componentes(estrutura, codigo).items():
        resultado.append((filho, qtd, nivel + 1))
        resultado.extend(explodir_bom(estrutura, filho, nivel + 1))
    return resultado


def exibir_bom(itens, estrutura, codigo):
    if codigo not in itens:
        print("Código não está presente em itens.")
        return

    print(f"{codigo} {itens[codigo]['descricao']}")

    for cod, qtd, nivel in explodir_bom(estrutura, codigo):
        recuo = "    " * nivel
        if cod not in itens:
            print(f"{recuo}{cod} (não cadastrado em itens) ... {qtd:g}")
            continue
        descricao = itens[cod]["descricao"]
        unidade = itens[cod]["unidade"]
        print(f"{recuo}{cod} {descricao} ... {qtd:g} {unidade}")