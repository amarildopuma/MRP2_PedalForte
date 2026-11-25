from utils import cabecalho, formatar_moeda, ler_float, ler_texto
from mps import SEMANAS

# Estruturas deste modulo:
#   centros  = {"CT-03": {"descricao": "Montagem final",
#                         "capacidade": 16.0, "custo_hora": 40.0}}
#   roteiros = {"PA-001": {"centro": "CT-03", "tempo": 0.5}}
# O roteiro tem uma unica operacao: centro que produz o item e tempo
# (em horas) para fazer UMA unidade (RF06).


def validar_codigo_centro(codigo):
    partes = codigo.split("-")
    return len(partes) == 2 and partes[0] == "CT" and partes[1].isdigit()


def formatar_horas(valor):
    return f"{valor:.1f}".replace(".", ",")


def cadastrar_centro(centros):
    while True:
        codigo = ler_texto("Codigo do centro (ex: CT-01, 0 para voltar): ")
        codigo = codigo.upper()
        if codigo == "0":
            return
        if not validar_codigo_centro(codigo):
            print("Codigo invalido. Use o formato CT-numero.")
            continue
        break

    if codigo in centros:
        print("Centro ja existe: os dados serao atualizados.")

    centros[codigo] = {
        "descricao": ler_texto("Descricao: "),
        "capacidade": ler_float("Capacidade (horas/semana): ", 0.01),
        "custo_hora": ler_float("Custo-hora (R$): ", 0.01),
    }
    print(f"Centro {codigo} salvo.")


def listar_centros(centros):
    cabecalho("CENTROS DE TRABALHO")
    if not centros:
        print("Nenhum centro cadastrado.")
        return
    print(f"{'Centro':<8}{'Descricao':<26}{'h/semana':>10}{'R$/hora':>10}")
    for codigo, dados in centros.items():
        print(f"{codigo:<8}{dados['descricao']:<26}"
              f"{formatar_horas(dados['capacidade']):>10}"
              f"{formatar_moeda(dados['custo_hora']):>10}")


def cadastrar_roteiro(itens, centros, roteiros):
    if not centros:
        print("Cadastre um centro de trabalho primeiro.")
        return

    while True:
        codigo = ler_texto("Codigo do item fabricado (0 para voltar): ")
        codigo = codigo.upper()
        if codigo == "0":
            return
        if codigo not in itens:
            print("Item nao encontrado.")
            continue
        if itens[codigo]["tipo"] == "MP":
            print("MP e comprada: so itens PA e SA tem roteiro.")
            continue
        break

    while True:
        centro = ler_texto("Centro que produz o item (0 para voltar): ")
        centro = centro.upper()
        if centro == "0":
            return
        if centro not in centros:
            print("Centro nao encontrado.")
            continue
        break

    tempo = ler_float("Tempo por unidade (horas): ", 0.01)
    roteiros[codigo] = {"centro": centro, "tempo": tempo}
    print(f"Roteiro de {codigo} salvo.")


def listar_roteiros(itens, centros, roteiros):
    cabecalho("ROTEIROS DE OPERACAO")
    if not roteiros:
        print("Nenhum roteiro cadastrado.")
        return
    print(f"{'Item':<8}{'Descricao':<26}{'Centro':<8}{'h/un':>8}")
    for codigo, dados in roteiros.items():
        descricao = itens[codigo]["descricao"] if codigo in itens else "?"
        print(f"{codigo:<8}{descricao:<26}{dados['centro']:<8}"
              f"{dados['tempo']:>8.2f}")


def calcular_carga(ordens, roteiros, codigo_centro):    
    carga = [0.0] * SEMANAS
    for ordem in ordens:
        if ordem["tipo"] != "OP" or ordem["status"] == "ENCERRADA":
            continue
        roteiro = roteiros.get(ordem["item"])
        if roteiro is None or roteiro["centro"] != codigo_centro:
            continue
        semana = max(1, ordem["sem_liberacao"])
        if semana <= SEMANAS:
            carga[semana - 1] += ordem["quantidade"] * roteiro["tempo"]
    return [round(horas, 4) for horas in carga]


def semanas_sobrecarregadas(carga, capacidade):
    """Lista de semanas (1 a 8) em que a carga supera a capacidade."""
    return [i + 1 for i, horas in enumerate(carga) if horas > capacidade]


def exibir_crp(centros, roteiros, ordens, codigo_centro):
    """RF12: carga x capacidade de um centro, semana a semana."""
    if codigo_centro not in centros:
        print("Centro nao encontrado.")
        return

    centro = centros[codigo_centro]
    capacidade = centro["capacidade"]
    carga = calcular_carga(ordens, roteiros, codigo_centro)

    print(f"CARGA x CAPACIDADE - {codigo_centro} {centro['descricao']} "
          f"({formatar_horas(capacidade)} h/semana)")
    print(f"{'Sem':<5}{'Carga(h)':>9}{'Uso(%)':>8}")
    for semana, horas in enumerate(carga, start=1):
        uso = horas / capacidade * 100
        barra = "#" * round(uso / 10)
        aviso = " SOBRECARGA" if horas > capacidade else ""
        print(f"{semana:<5}{formatar_horas(horas):>9}{uso:>8.0f}  "
              f"{barra}{aviso}")

    sobrecarga = semanas_sobrecarregadas(carga, capacidade)
    if sobrecarga:
        lista = ", ".join(str(s) for s in sobrecarga)
        rotulo = "na semana" if len(sobrecarga) == 1 else "nas semanas"
        print(f"Sugestao: antecipar OPs ou programar hora extra "
              f"{rotulo} {lista}.")
    else:
        print("Nenhuma semana com sobrecarga.")
