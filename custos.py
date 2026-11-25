from utils import cabecalho, formatar_moeda


def obter_mao_de_obra(centros, roteiros, codigo):
    """Devolve (centro, horas, custo) da mao de obra de UMA unidade.

    Item sem roteiro (ou com centro que nao existe) tem mao de obra zero.
    """
    roteiro = roteiros.get(codigo)
    if roteiro is None or roteiro["centro"] not in centros:
        return None, 0.0, 0.0
    centro = roteiro["centro"]
    horas = roteiro["tempo"]
    return centro, horas, round(horas * centros[centro]["custo_hora"], 4)


def calcular_custo_padrao(itens, estrutura, centros, roteiros, codigo):
    """RF13: custo padrao de um item, de forma recursiva.

    MP: o custo unitario cadastrado.
    PA e SA: soma(qtd x custo padrao de cada componente) + mao de obra.
    """
    if itens[codigo]["tipo"] == "MP":
        return itens[codigo]["custo"]

    materiais = 0.0
    for filho, qtd in estrutura.get(codigo, {}).items():
        materiais += qtd * calcular_custo_padrao(
            itens, estrutura, centros, roteiros, filho)

    _, _, mao_de_obra = obter_mao_de_obra(centros, roteiros, codigo)
    return round(materiais + mao_de_obra, 4)


def exibir_custo_padrao(itens, estrutura, centros, roteiros, codigo):
    if codigo not in itens:
        print("Item nao encontrado.")
        return
    if itens[codigo]["tipo"] == "MP":
        print("MP e comprada: o custo padrao vale so para PA e SA.")
        return

    cabecalho(f"CUSTO PADRAO - {codigo} {itens[codigo]['descricao']}")
    print(f"{'Item':<8}{'Descricao':<26}{'Qtde':>6}"
          f"{'Custo un.':>14}{'Total':>14}")

    for filho, qtd in estrutura.get(codigo, {}).items():
        custo = calcular_custo_padrao(
            itens, estrutura, centros, roteiros, filho)
        print(f"{filho:<8}{itens[filho]['descricao']:<26}{qtd:>6g}"
              f"{formatar_moeda(custo):>14}"
              f"{formatar_moeda(qtd * custo):>14}")

    centro, horas, mao_de_obra = obter_mao_de_obra(
        centros, roteiros, codigo)
    if centro is not None:
        texto = f"Mao de obra {centro} {horas:g} h"
        custo_hora = centros[centro]["custo_hora"]
        print(f"{texto:<40}{formatar_moeda(custo_hora):>14}"
              f"{formatar_moeda(mao_de_obra):>14}")

    print("-" * 68)
    total = calcular_custo_padrao(
        itens, estrutura, centros, roteiros, codigo)
    print(f"{'CUSTO PADRAO TOTAL':<54}{formatar_moeda(total):>14}")
