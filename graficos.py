import os

from capacidade import calcular_carga, semanas_sobrecarregadas
from estoque import obter_saldo
from mps import SEMANAS

try:
    import matplotlib.pyplot as plt
except ImportError:  # o sistema continua funcionando sem os graficos
    plt = None

PASTA_GRAFICOS = "graficos"
AZUL = "#2a6fbb"
LARANJA = "#e07b00"
VERMELHO = "#c0392b"
CINZA = "#7f8c8d"


def _matplotlib_disponivel():
    if plt is None:
        print("A biblioteca matplotlib nao esta instalada.")
        print("Instale com: pip install matplotlib")
        return False
    return True


def _salvar_e_mostrar(figura, nome_arquivo, mostrar):
    """Salva o grafico em PNG (RF16) e, se pedido, abre na tela."""
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    caminho = os.path.join(PASTA_GRAFICOS, nome_arquivo)
    figura.savefig(caminho, dpi=150, bbox_inches="tight")
    print(f"Grafico salvo em {caminho}")
    if mostrar:
        plt.show()
    plt.close(figura)


def grafico_posicao_estoque(itens, estoque, mostrar=True):
    """Barras: saldo atual x estoque de seguranca de cada item."""
    if not _matplotlib_disponivel():
        return
    if not itens:
        print("Nenhum item cadastrado.")
        return

    codigos = list(itens)
    saldos = [obter_saldo(estoque, c) for c in codigos]
    segurancas = [itens[c]["estoque_seguranca"] for c in codigos]
    cores = [VERMELHO if saldo < seg else AZUL
             for saldo, seg in zip(saldos, segurancas)]
    posicoes = list(range(len(codigos)))
    largura = 0.4

    figura, eixo = plt.subplots(figsize=(11, 5))
    eixo.bar([p - largura / 2 for p in posicoes], saldos, largura,
             color=cores, label="Saldo atual")
    eixo.bar([p + largura / 2 for p in posicoes], segurancas, largura,
             color=LARANJA, label="Estoque de seguranca")
    eixo.set_xticks(posicoes)
    eixo.set_xticklabels(codigos, rotation=45, ha="right")
    eixo.set_ylabel("Quantidade")
    eixo.set_title("Posicao de estoque (vermelho = abaixo da seguranca)")
    eixo.legend()
    _salvar_e_mostrar(figura, "posicao_estoque.png", mostrar)


def grafico_estoque_projetado(itens, registros, codigo, mostrar=True):
    """Linha: estoque projetado do item nas 8 semanas do MRP."""
    if not _matplotlib_disponivel():
        return
    if codigo not in registros:
        print("Item sem registro MRP. Execute o MRP primeiro.")
        return

    projetado = registros[codigo]["ep"]
    seguranca = itens[codigo]["estoque_seguranca"]
    semanas = list(range(1, SEMANAS + 1))

    figura, eixo = plt.subplots(figsize=(9, 5))
    eixo.plot(semanas, projetado, marker="o", color=AZUL,
              label="Estoque projetado")
    eixo.axhline(seguranca, color=VERMELHO, linestyle="--",
                 label=f"Estoque de seguranca ({seguranca:g})")
    eixo.set_xticks(semanas)
    eixo.set_xlabel("Semana")
    eixo.set_ylabel("Quantidade")
    eixo.set_title(f"Estoque projetado - {codigo} "
                   f"{itens[codigo]['descricao']}")
    eixo.legend()
    _salvar_e_mostrar(figura, f"estoque_projetado_{codigo}.png", mostrar)


def contar_ordens_por_semana(ordens):
    """Devolve (op, oc): quantas ordens chegam em cada semana (1 a 8).

    Ordens encerradas ja chegaram e ficam de fora.
    """
    op = [0] * SEMANAS
    oc = [0] * SEMANAS
    for ordem in ordens:
        semana = ordem["sem_entrega"]
        if ordem["status"] == "ENCERRADA" or not 1 <= semana <= SEMANAS:
            continue
        if ordem["tipo"] == "OP":
            op[semana - 1] += 1
        else:
            oc[semana - 1] += 1
    return op, oc


def grafico_ordens_por_semana(ordens, mostrar=True):
    """Barras empilhadas: OP e OC por semana de entrega."""
    if not _matplotlib_disponivel():
        return
    if not ordens:
        print("Nenhuma ordem. Execute o MRP primeiro.")
        return

    op, oc = contar_ordens_por_semana(ordens)
    semanas = list(range(1, SEMANAS + 1))

    figura, eixo = plt.subplots(figsize=(9, 5))
    eixo.bar(semanas, op, color=AZUL, label="OP (producao)")
    eixo.bar(semanas, oc, bottom=op, color=LARANJA, label="OC (compra)")
    eixo.set_xticks(semanas)
    eixo.set_xlabel("Semana de entrega")
    eixo.set_ylabel("Numero de ordens")
    eixo.set_title("Ordens por semana de entrega")
    eixo.legend()
    _salvar_e_mostrar(figura, "ordens_por_semana.png", mostrar)


def grafico_carga_capacidade(centros, roteiros, ordens, codigo_centro,
                             mostrar=True):
    """Barras: carga do centro por semana x capacidade (sobrecarga em
    vermelho)."""
    if not _matplotlib_disponivel():
        return
    if codigo_centro not in centros:
        print("Centro nao encontrado.")
        return

    capacidade = centros[codigo_centro]["capacidade"]
    carga = calcular_carga(ordens, roteiros, codigo_centro)
    sobrecarga = semanas_sobrecarregadas(carga, capacidade)
    semanas = list(range(1, SEMANAS + 1))
    cores = [VERMELHO if s in sobrecarga else AZUL for s in semanas]

    figura, eixo = plt.subplots(figsize=(9, 5))
    eixo.bar(semanas, carga, color=cores)
    eixo.axhline(capacidade, color=CINZA, linestyle="--",
                 label=f"Capacidade ({capacidade:g} h/semana)")
    eixo.set_xticks(semanas)
    eixo.set_xlabel("Semana")
    eixo.set_ylabel("Horas")
    eixo.set_title(f"Carga x capacidade - {codigo_centro} "
                   f"{centros[codigo_centro]['descricao']} "
                   "(vermelho = sobrecarga)")
    eixo.legend()
    _salvar_e_mostrar(figura, f"carga_{codigo_centro}.png", mostrar)
