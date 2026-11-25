import csv
import os

from estoque import obter_saldo

PASTA_EXPORTACAO = "exportacoes"


def _caminho(nome_arquivo):
    os.makedirs(PASTA_EXPORTACAO, exist_ok=True)
    return os.path.join(PASTA_EXPORTACAO, nome_arquivo)


def exportar_posicao_estoque(itens, estoque,
                             nome_arquivo="posicao_estoque.csv"):
    """RF14: saldo atual x estoque de seguranca de todos os itens."""
    caminho = _caminho(nome_arquivo)
    colunas = ["codigo", "descricao", "tipo", "unidade", "saldo",
               "estoque_seguranca", "situacao"]
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        for codigo, dados in itens.items():
            saldo = obter_saldo(estoque, codigo)
            abaixo = saldo < dados["estoque_seguranca"]
            escritor.writerow({
                "codigo": codigo,
                "descricao": dados["descricao"],
                "tipo": dados["tipo"],
                "unidade": dados["unidade"],
                "saldo": saldo,
                "estoque_seguranca": dados["estoque_seguranca"],
                "situacao": "ABAIXO" if abaixo else "OK",
            })
    print(f"Posicao de estoque exportada em {caminho}")
    return caminho


def exportar_ordens(ordens, nome_arquivo="ordens.csv"):
    """RF14: lista de todas as ordens (OP e OC)."""
    caminho = _caminho(nome_arquivo)
    colunas = ["numero", "tipo", "item", "quantidade", "sem_liberacao",
               "sem_entrega", "status"]
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(ordens)
    print(f"Ordens exportadas em {caminho}")
    return caminho
