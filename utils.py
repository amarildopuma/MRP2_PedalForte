from datetime import date, datetime

def ler_int(msg, minimo = None):
    while True:
        quantidade=input(msg)
        try:
            quantidade=int(quantidade)
            if minimo is None or quantidade >= minimo:
                return quantidade
            else:
                print("Valor menor que o minimo")
        except ValueError:
            print("Valor não se encaixa em int")
    
def ler_float(msg, minimo = None):
    while True:
        numero = input(msg)
        numero = numero.replace(',','.')
        try:
            numero = float(numero)
            if minimo is None or numero >= minimo:
                return numero
            else:
                print("numero menor q o minimo")
        except ValueError:
            print("Valor não se encaixa em float")
        
def ler_texto(msg):
    while True:
        texto = input(msg).strip()
        if len(texto)== 0:
            print("Digite algo")
        else:
            return texto

def ler_opcao(msg, opcoes_validas):
    while True:
        opcao = input(msg).strip().upper()
        if opcao in opcoes_validas:
            return opcao
        else:
            print("Opção inválida")

def validar_codigo(codigo):
    partes = codigo.split("-")
    if len(partes) != 2:
        return False
    if partes[0] not in ["PA", "SA", "MP"]:
        return False
    return partes[1].isdigit()

def tipo_do_codigo(codigo):
    return codigo.split("-")[0]

def linha():
    print("-" * 50)

def cabecalho(titulo):
    print("=" * 50)
    print(titulo.center(50))
    print("=" * 50)

def data_hoje():
    return date.today().isoformat()          

def formatar_data(data):
    return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")

def formatar_moeda(valor):
    texto = f"{valor:,.2f}"                  
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"                     