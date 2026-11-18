from utils import ler_texto, validar_codigo, tipo_do_codigo, ler_int, ler_float, formatar_moeda, ler_opcao
from persistencia import carregar_json, salvar_json

def cadastrar_item(itens):
    while True:
        codigo = ler_texto("Código do item: ").upper()
        if not validar_codigo(codigo):
            print("Código inválido, tente de novo!")
            continue
        if codigo in itens:
            print("item ja existe")
            continue
        break


    itens[codigo] = {
        "descricao" : ler_texto("Descrição: "),
        "tipo": tipo_do_codigo(codigo),
        "unidade": ler_texto("Unidade: "),
        "custo": ler_float("Custo: ", 0.01),
        "lead_time": ler_int("Lead time (semanas): ", 0),
        "estoque_seguranca": ler_int("Estoque de segurança: ", 0),
        "lote_minimo": ler_int("Lote mínimo: ", 1),
    }


def listar_itens(itens):
    if not itens:
        print("Nenhum item cadastrado.")
        return

    for codigo, dados in itens.items():
        print(
            f"{codigo}  {dados['descricao']}  ({dados['tipo']})  "
            f"{dados['unidade']}  {formatar_moeda(dados['custo'])}  "
            f"{dados['lead_time']}  {dados['estoque_seguranca']}  "
            f"{dados['lote_minimo']}"
        )


def alterar_item(itens):
    while True:
        codigo = ler_texto("Código do item: ").upper()
        if codigo not in itens:
            print("Item não encontrado.")
            continue
        break

    print("1. Descrição")
    print("2. Unidade")
    print("3. Custo")
    print("4. Lead time")
    print("5. Estoque de segurança")
    print("6. Lote mínimo")
    campo = ler_opcao("Campo a alterar [1-6]: ",
                      ["1", "2", "3", "4", "5", "6"])

    if campo == "1":
        itens[codigo]["descricao"] = ler_texto("Nova descrição: ")
    elif campo == "2":
        itens[codigo]["unidade"] = ler_texto("Nova unidade: ")
    elif campo == "3":
        itens[codigo]["custo"] = ler_float("Novo custo: ", 0.01)
    elif campo == "4":
        itens[codigo]["lead_time"] = ler_int("Novo lead time: ", 0)
    elif campo == "5":
        itens[codigo]["estoque_seguranca"] = ler_int("Novo estoque: ", 0)
    elif campo == "6":
        itens[codigo]["lote_minimo"] = ler_int("Novo lote mínimo: ", 1)

    print(f"Item {codigo} alterado.")


def item_existe(itens, codigo):
    if codigo in itens:
        return True
    else:
        return False


def buscar_item(itens, codigo):
    if item_existe(itens, codigo):
        return itens[codigo]
    return None

if __name__ == "__main__":
    itens = carregar_json("itens.json")
    cadastrar_item(itens)
    salvar_json("itens.json", itens)
    listar_itens(itens)