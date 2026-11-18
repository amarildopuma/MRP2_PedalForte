import json
import os

PASTA_DATA = "data"

def carregar_json(nome_arquivo):
    caminho = os.path.join(PASTA_DATA, nome_arquivo)
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Aviso!!: Arquivo corrompido '{nome_arquivo}' ou vázio")
        return {}


def salvar_json(nome_arquivo, dados):
    os.makedirs(PASTA_DATA, exist_ok=True)
    caminho = os.path.join(PASTA_DATA, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)