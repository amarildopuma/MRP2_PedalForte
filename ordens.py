from estoque import obter_saldo, registrar_movimentacao
from utils import cabecalho


STATUS_APAGAVEIS = ["PLANEJADA", "ATRASADA"]


def apagar_ordens_planejadas(ordens):
    """RN08: ordens PLANEJADAS (e ATRASADAS) sao apagadas a cada MRP."""
    ordens[:] = [o for o in ordens if o["status"] not in STATUS_APAGAVEIS]


def proximo_numero(ordens, tipo):
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


def verificar_componentes(estrutura, estoque, item, quantidade):
    """Lista os componentes que faltam para produzir `quantidade` do item.
    """
    faltas = []#se tiver vazia da para produzir
    for componente, qtd in estrutura.get(item, {}).items():
        necessario = round(qtd * quantidade, 4)
        saldo = obter_saldo(estoque, componente)
        if saldo < necessario:
            faltas.append((componente, necessario, saldo))
    return faltas


def apontar_producao(itens, estrutura, estoque, movimentos, ordens,
                     numero):
    ordem = buscar_ordem(ordens, numero)
    if ordem is None:
        print("Ordem nao encontrada.")
        return False
    if ordem["tipo"] != "OP":
        print("So e possivel apontar producao de OP. "
              "Para OC, use 'Receber compra'.")
        return False
    if ordem["status"] != "LIBERADA":
        print(f"Nao e possivel: a ordem {numero} esta {ordem['status']} "
              "(precisa estar LIBERADA).")
        return False

    item = ordem["item"]
    quantidade = ordem["quantidade"]

    faltas = verificar_componentes(estrutura, estoque, item, quantidade)
    if faltas:
        print(f"ERRO: faltam componentes para a {numero}. "
              "Apontamento rejeitado.")
        for componente, necessario, saldo in faltas:
            print(f"  {componente}: necessario {necessario:g}, "
                  f"saldo {saldo:g}")
        return False

    for componente, qtd in estrutura.get(item, {}).items():
        registrar_movimentacao(estoque, movimentos, componente, "SAIDA",
                               round(qtd * quantidade, 4),
                               f"{numero} ({item})")
    registrar_movimentacao(estoque, movimentos, item, "ENTRADA",
                           quantidade, f"{numero} (apontamento)")

    ordem["status"] = "ENCERRADA"
    print(f"Producao apontada: {quantidade:g} x {item}. "
          f"Ordem {numero} ENCERRADA.")
    return True


def receber_compra(estoque, movimentos, ordens, numero):
    """Encerra uma OC liberada dando entrada da MP comprada no estoque."""
    ordem = buscar_ordem(ordens, numero)
    if ordem is None:
        print("Ordem nao encontrada.")
        return False
    if ordem["tipo"] != "OC":
        print("Isto vale so para OC. Para OP, use 'Apontar producao'.")
        return False
    if ordem["status"] != "LIBERADA":
        print(f"Nao e possivel: a ordem {numero} esta {ordem['status']} "
              "(precisa estar LIBERADA).")
        return False

    registrar_movimentacao(estoque, movimentos, ordem["item"], "ENTRADA",
                           ordem["quantidade"], f"{numero} (recebimento)")
    ordem["status"] = "ENCERRADA"
    print(f"Compra recebida: {ordem['quantidade']:g} x {ordem['item']}. "
          f"Ordem {numero} ENCERRADA.")
    return True
