from utils import ler_texto, ler_int, cabecalho
from itens import item_existe

SEMANAS = 8

# Estrutura do MPS (RF07):
#   mps = {"PA-001": [0, 0, 10, 30, 0, 20, 0, 0]}
#   chave  = código do produto acabado
#   valor  = lista com a demanda das 8 semanas (posição 0 = semana 1)


def obter_demanda(mps, codigo):
    """Devolve a lista de 8 semanas. Produto sem MPS tem demanda zero."""
    return mps.get(codigo, [0] * SEMANAS)


def pedir_codigo_pa(itens):
    """Pede um código até ser de um item que existe e é PA."""
    while True:
        codigo = ler_texto("Codigo do item (0 para voltar): ").upper()
        if codigo == "0":
            return
        if not item_existe(itens, codigo):
            print("Item nao encontrado.")
            continue
        if itens[codigo]["tipo"] != "PA":
            print("O MPS aceita apenas produtos acabados (PA).")
            continue
        return codigo


def cadastrar_mps(itens, mps):
    codigo = pedir_codigo_pa(itens)
    if codigo is None:
        return

    demanda = []
    for semana in range(1, SEMANAS + 1):
        demanda.append(ler_int(f"Demanda da semana {semana}: ", 0))

    mps[codigo] = demanda
    print(f"MPS de {codigo} cadastrado.")


def alterar_mps(itens, mps):
    if not mps:
        print("Nenhum MPS cadastrado.")
        return

    while True:
        codigo = ler_texto("Codigo do item (0 para voltar): ").upper()
        if codigo == "0":
            return
        if codigo not in mps:
            print("Esse produto nao tem MPS cadastrado.")
            continue
        break

    semana = ler_int(f"Semana a alterar [1-{SEMANAS}]: ", 1)
    while semana > SEMANAS:
        print(f"A semana deve ser de 1 a {SEMANAS}.")
        semana = ler_int(f"Semana a alterar [1-{SEMANAS}]: ", 1)

    mps[codigo][semana - 1] = ler_int("Nova demanda: ", 0)
    print(f"Semana {semana} de {codigo} alterada.")

    semana = ler_int(f"Semana a alterar [1-{SEMANAS}]: ", 1)
    while semana > SEMANAS:
        print(f"A semana deve ser de 1 a {SEMANAS}.")
        semana = ler_int(f"Semana a alterar [1-{SEMANAS}]: ", 1)

    mps[codigo][semana - 1] = ler_int("Nova demanda: ", 0)
    print(f"Semana {semana} de {codigo} alterada.")


def exibir_mps(itens, mps):
    cabecalho("PLANO MESTRE DE PRODUCAO (MPS)")
    if not mps:
        print("Nenhum MPS cadastrado.")
        return

    semanas = "".join(f"{s:>5}" for s in range(1, SEMANAS + 1))
    print(f"{'Item':<8}{'Descricao':<26}{semanas}")
    for codigo, demanda in mps.items():
        valores = "".join(f"{d:>5}" for d in demanda)
        descricao = itens[codigo]["descricao"] if codigo in itens else "?"
        print(f"{codigo:<8}{descricao:<26}{valores}")


if __name__ == "__main__":
    itens = {
        "PA-001": {"descricao": "Bicicleta Aro 29 MTB", "tipo": "PA",
                   "unidade": "un", "custo": 0.0, "lead_time": 1,
                   "estoque_seguranca": 0, "lote_minimo": 1},
        "MP-300": {"descricao": "Guidao", "tipo": "MP", "unidade": "un",
                   "custo": 45.0, "lead_time": 2,
                   "estoque_seguranca": 10, "lote_minimo": 30},
    }
    mps = {"PA-001": [0, 10, 30, 0, 20, 0, 0, 0]}

    exibir_mps(itens, mps)
    print(obter_demanda(mps, "PA-001"))   # [0, 10, 30, 0, 20, 0, 0, 0]
    print(obter_demanda(mps, "PA-002"))   # [0, 0, 0, 0, 0, 0, 0, 0]

    # Testes interativos (descomente para rodar):
    # cadastrar_mps(itens, mps)    # tente MP-300 (tem que recusar)
    # alterar_mps(itens, mps)
    # exibir_mps(itens, mps)