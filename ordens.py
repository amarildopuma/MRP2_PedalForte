from utils import cabecalho

STATUS_APAGAVEIS = ["PLANEJADA", "ATRASADA"]


def apagar_ordens_planejadas(ordens):
    """RN08: ordens PLANEJADAS (e ATRASADAS) sao apagadas a cada MRP."""
    ordens[:] = [o for o in ordens if o["status"] not in STATUS_APAGAVEIS]


def proximo_numero(ordens, tipo):
    """Devolve o proximo numero livre: OP-0001, OC-0004..."""
    maior = 0
    for ordem in ordens:
        if ordem["tipo"] == tipo:
            maior = max(maior, int(ordem["numero"].split("-")[1]))
    return f"{tipo}-{maior + 1:04d}"


def criar_ordem(ordens, tipo, item, quantidade, sem_liberacao, sem_entrega,
                status="PLANEJADA"):
    ordem = {
        "numero": proximo_numero(ordens, tipo),
        "tipo": tipo,
        "item": item,
        "quantidade": quantidade,
        "sem_liberacao": sem_liberacao,
        "sem_entrega": sem_entrega,
        "status": status,
    }
    ordens.append(ordem)
    return ordem


def buscar_ordem(ordens, numero):
    for ordem in ordens:
        if ordem["numero"] == numero:
            return ordem
    return None


def listar_excecoes(ordens):
    atrasadas = [o for o in ordens if o["status"] == "ATRASADA"]
    if atrasadas:
        print(f"{len(atrasadas)} mensagens de excecao: ordens com "
              "liberacao antes da semana 1.")
    return atrasadas


def listar_ordens(ordens):
    cabecalho("ORDENS DE PRODUCAO E DE COMPRA")
    if not ordens:
        print("Nenhuma ordem.")
        return
    print(f"{'Ordem':<10}{'Tipo':<6}{'Item':<8}{'Qtde':>8}"
          f"{'Liberar':>9}{'Entregar':>10}  Status")
    for o in ordens:
        print(f"{o['numero']:<10}{o['tipo']:<6}{o['item']:<8}"
              f"{o['quantidade']:>8g}{'S' + str(o['sem_liberacao']):>9}"
              f"{'S' + str(o['sem_entrega']):>10}  {o['status']}")
    listar_excecoes(ordens)


def mudar_status(ordens, numero, status_validos, novo_status):
    ordem = buscar_ordem(ordens, numero)
    if ordem is None:
        print("Ordem nao encontrada.")
        return False
    if ordem["status"] not in status_validos:
        print(f"Nao e possivel: a ordem {numero} esta {ordem['status']}.")
        return False
    ordem["status"] = novo_status
    print(f"Ordem {numero} agora esta {novo_status}.")
    return True


def firmar_ordem(ordens, numero):
    return mudar_status(ordens, numero, ["PLANEJADA", "ATRASADA"], "FIRME")


def liberar_ordem(ordens, numero):
    return mudar_status(ordens, numero, ["FIRME"], "LIBERADA")


def encerrar_ordem(ordens, numero):
    return mudar_status(ordens, numero, ["LIBERADA"], "ENCERRADA")