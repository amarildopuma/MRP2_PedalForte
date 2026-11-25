import csv
import json
import os

PASTA_DATA = "data"
CAMPOS_MOVIMENTO = ["data", "codigo", "tipo", "quantidade", "saldo",
                    "documento"]


def carregar_json(nome_arquivo):
    caminho = os.path.join(PASTA_DATA, nome_arquivo)
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Aviso!!: Arquivo corrompido '{nome_arquivo}' ou vazio")
        return {}


def salvar_json(nome_arquivo, dados):
    os.makedirs(PASTA_DATA, exist_ok=True)
    caminho = os.path.join(PASTA_DATA, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def carregar_movimentos():
    caminho = os.path.join(PASTA_DATA, "movimentos.csv")
    movimentos = []
    try:
        with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
            for linha in csv.DictReader(arquivo):
                linha["quantidade"] = float(linha["quantidade"])
                linha["saldo"] = float(linha["saldo"])
                movimentos.append(linha)
    except FileNotFoundError:
        pass
    return movimentos


def salvar_movimentos(movimentos):
    os.makedirs(PASTA_DATA, exist_ok=True)
    caminho = os.path.join(PASTA_DATA, "movimentos.csv")
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_MOVIMENTO)
        escritor.writeheader()
        escritor.writerows(movimentos)


def carregar_tudo():
    """Carrega todos os dados do sistema (chamado ao iniciar)."""
    itens = carregar_json("itens.json")
    estrutura = carregar_json("estrutura.json")
    estoque = carregar_json("estoque.json")
    mps = carregar_json("mps.json")
    ordens = carregar_json("ordens.json")
    if not ordens:  # arquivo ausente devolve {}, mas ordens e uma lista
        ordens = []
    movimentos = carregar_movimentos()
    centros = carregar_json("centros.json")
    roteiros = carregar_json("roteiros.json")
    return (itens, estrutura, estoque, mps, ordens, movimentos,
            centros, roteiros)


def salvar_tudo(itens, estrutura, estoque, mps, ordens, movimentos,
                centros, roteiros):
    """Grava todos os dados do sistema (chamado a cada alteracao)."""
    salvar_json("itens.json", itens)
    salvar_json("estrutura.json", estrutura)
    salvar_json("estoque.json", estoque)
    salvar_json("mps.json", mps)
    salvar_json("ordens.json", ordens)
    salvar_movimentos(movimentos)
    salvar_json("centros.json", centros)
    salvar_json("roteiros.json", roteiros)
