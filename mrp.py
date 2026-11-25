from mps import obter_demanda
from ordens import apagar_ordens_planejadas, criar_ordem, listar_excecoes


SEMANAS = 8


def ordenar_itens_por_tipo(itens):
    """RN04: primeiro os PA, depois os SA e por fim as MP."""
    ordenados = []
    for tipo in ["PA", "SA", "MP"]:
        for codigo in itens:
            if itens[codigo]["tipo"] == tipo:
                ordenados.append(codigo)
    return ordenados


def obter_recebimentos_programados(ordens, codigo):
    """RN08: so ordens FIRMES ou LIBERADAS contam como recebimento."""
    rp = [0] * SEMANAS
    for ordem in ordens:
        if (ordem["item"] == codigo
                and ordem["status"] in ["FIRME", "LIBERADA"]):
            semana = max(1, ordem["sem_entrega"])
            if semana <= SEMANAS:
                rp[semana - 1] += ordem["quantidade"]
    return rp


def calcular_necessidade_bruta(itens, estrutura, mps, registros, codigo):
    """PA: demanda do MPS. SA e MP: liberacoes dos pais x quantidade."""
    if itens[codigo]["tipo"] == "PA":
        return list(obter_demanda(mps, codigo))

    nb = [0] * SEMANAS
    for pai, filhos in estrutura.items():
        if codigo in filhos and pai in registros:
            qtd_por_pai = filhos[codigo]
            for i in range(SEMANAS):
                nb[i] += registros[pai]["lp_total"][i] * qtd_por_pai
    return nb


def calcular_registro_item(
        item,
        saldo_inicial,  # estoque atual do item (saldo em estoque.json)
        nb,  # necessidade bruta: quanto preciso em cada semana
        rp):  # recebimentos programados: ordens FIRME/LIBERADA a chegar
    """Aplica RN05, RN06 e RN07 semana a semana."""
    seguranca = item["estoque_seguranca"]  # ES: estoque de seguranca
    lote_minimo = item["lote_minimo"]  # menor quantidade por ordem (RN06)
    lead_time = item["lead_time"]  # semanas entre liberar e receber (RN07)

    nl = [0] * SEMANAS  # necessidade liquida: o que falta de fato (RN05)
    rpl = [0] * SEMANAS  # recebimentos planejados: quanto pedir (RN06)
    ep = [0] * SEMANAS  # estoque projetado: sobra no fim da semana
    lp = [0] * SEMANAS  # liberacao planejada: semana de iniciar (RN07)
    lp_total = [0] * SEMANAS  # lp + atrasadas (alimenta nb dos filhos)
    planejadas = []  # ordens a criar: (sem_liberacao, sem_entrega, qtd)

    ep_anterior = saldo_inicial  # estoque projetado da semana anterior
    for i in range(SEMANAS):  # i = posicao na lista (semana - 1)
        # RN05
        nl[i] = max(0, nb[i] + seguranca - (ep_anterior + rp[i]))

        # RN06
        if nl[i] > 0:
            rpl[i] = max(nl[i], lote_minimo)

        ep[i] = round(ep_anterior + rp[i] + rpl[i] - nb[i], 4)
        ep_anterior = ep[i]

        # RN07: liberacao = semana do recebimento - lead time
        if rpl[i] > 0:
            sem_entrega = i + 1  # semana de chegada (posicao + 1)
            sem_liberacao = sem_entrega - lead_time  # semana de iniciar
            planejadas.append((sem_liberacao, sem_entrega, rpl[i]))
            if sem_liberacao >= 1:
                lp[sem_liberacao - 1] += rpl[i]
                lp_total[sem_liberacao - 1] += rpl[i]
            else:
                lp_total[0] += rpl[i]  # atrasada: a necessidade cai na sem. 1

    return {
        "saldo_inicial": saldo_inicial,
        "nb": nb, "rp": rp, "ep": ep, "nl": nl, "rpl": rpl,
        "lp": lp, "lp_total": lp_total, "planejadas": planejadas,
    }



def gerar_ordens_do_registro(ordens, itens, codigo, registro):
    tipo_ordem = "OC" if itens[codigo]["tipo"] == "MP" else "OP"
    for sem_lib, sem_ent, qtd in registro["planejadas"]:
        status = "ATRASADA" if sem_lib < 1 else "PLANEJADA"
        criar_ordem(ordens, tipo_ordem, codigo, qtd, sem_lib, sem_ent, status)


def executar_mrp(itens, estrutura, estoque, mps, ordens):
    apagar_ordens_planejadas(ordens)  # RN08
    registros = {}

    for codigo in ordenar_itens_por_tipo(itens):
        saldo = estoque.get(codigo, 0)
        nb = calcular_necessidade_bruta(itens, estrutura, mps,
                                        registros, codigo)
        rp = obter_recebimentos_programados(ordens, codigo)
        registro = calcular_registro_item(itens[codigo], saldo, nb, rp)
        registros[codigo] = registro
        gerar_ordens_do_registro(ordens, itens, codigo, registro)

    print("MRP executado.")
    listar_excecoes(ordens)
    return registros


def _linha(rotulo, valores):
    print(f"{rotulo:<22}" + "".join(f"{v:>6g}" for v in valores))


def exibir_registro_mrp(itens, registros, codigo):
    if codigo not in registros:
        print("Item sem registro MRP. Execute o MRP primeiro.")
        return

    item = itens[codigo]
    reg = registros[codigo]
    print(f"REGISTRO MRP - {codigo} {item['descricao']}")
    print(f"Lead time: {item['lead_time']} sem | "
          f"Est. seguranca: {item['estoque_seguranca']} | "
          f"Lote min.: {item['lote_minimo']} | "
          f"Estoque: {reg['saldo_inicial']:g}")

    semanas = "".join(f"{s:>6}" for s in range(1, SEMANAS + 1))
    print(f"{'Semana':<22}{semanas}")
    _linha("Necessidade bruta", reg["nb"])
    _linha("Receb. programados", reg["rp"])
    _linha("Estoque projetado", reg["ep"])
    _linha("Necessidade liquida", reg["nl"])
    _linha("Receb. planejados", reg["rpl"])
    _linha("Liberacao planejada", reg["lp"])
