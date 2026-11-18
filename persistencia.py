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
if __name__ == "__main__":
    print(carregar_json("teste.json"))      # o dicionário
    print(carregar_json("naoexiste.json"))  # {}

def salvar_json(nome_arquivo, dados):
    os.makedirs(PASTA_DATA, exist_ok=True)
    caminho = os.path.join(PASTA_DATA, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    itens = {"PA-001": {"descricao": "Bicicleta Aro 29", "custo": 792.6}}
    salvar_json("itens.json", itens)
    print(carregar_json("itens.json"))