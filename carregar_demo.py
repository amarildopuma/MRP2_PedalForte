from persistencia import salvar_tudo


def item(descricao, tipo, unidade, custo, lead_time, seguranca, lote):
    return {"descricao": descricao, "tipo": tipo, "unidade": unidade,
            "custo": custo, "lead_time": lead_time,
            "estoque_seguranca": seguranca, "lote_minimo": lote}


itens = {
    "PA-001": item("Bicicleta Aro 29 MTB", "PA", "un", 792.6, 1, 0, 1),
    "PA-002": item("Bicicleta Aro 29 Urbana", "PA", "un", 529.6, 1, 0, 1),
    "SA-010": item("Quadro aro 29 soldado", "SA", "un", 128.0, 1, 5, 20),
    "SA-020": item("Roda aro 29 montada", "SA", "un", 139.8, 1, 10, 80),
    "MP-100": item("Tubo de aco carbono", "MP", "m", 32.0, 2, 30, 100),
    "MP-101": item("Tinta epoxi", "MP", "l", 24.0, 2, 5, 10),
    "MP-200": item("Aro 29 aluminio", "MP", "un", 60.0, 2, 20, 100),
    "MP-201": item("Raio inox", "MP", "un", 0.55, 1, 200, 500),
    "MP-202": item("Pneu 29 x 2.20", "MP", "un", 40.0, 2, 20, 50),
    "MP-300": item("Guidao", "MP", "un", 45.0, 2, 10, 30),
    "MP-301": item("Kit transmissao 12v", "MP", "un", 320.0, 3, 10, 20),
    "MP-302": item("Selim", "MP", "un", 35.0, 2, 10, 30),
    "MP-303": item("Paralama (par)", "MP", "un", 22.0, 2, 10, 40),
}

estrutura = {
    "PA-001": {"SA-010": 1, "SA-020": 2, "MP-300": 1, "MP-301": 1},
    "PA-002": {"SA-010": 1, "SA-020": 2, "MP-300": 1, "MP-302": 1,
               "MP-303": 1},
    "SA-010": {"MP-100": 3, "MP-101": 0.5},
    "SA-020": {"MP-200": 1, "MP-201": 36, "MP-202": 1},
}

centros = {
    "CT-01": {"descricao": "Soldagem de quadros", "capacidade": 40.0,
              "custo_hora": 50.0},
    "CT-02": {"descricao": "Montagem de rodas", "capacidade": 40.0,
              "custo_hora": 25.0},
    "CT-03": {"descricao": "Montagem final", "capacidade": 16.0,
              "custo_hora": 40.0},
}

roteiros = {
    "SA-010": {"centro": "CT-01", "tempo": 0.4},
    "SA-020": {"centro": "CT-02", "tempo": 0.8},
    "PA-001": {"centro": "CT-03", "tempo": 0.5},
    "PA-002": {"centro": "CT-03", "tempo": 0.5},
}

# --- Estoque e kardex -------------------------------------------------
# Saldo final desejado de cada item e o historico de movimentos. O saldo
# inicial de cada item e calculado para o kardex fechar certinho no saldo
# final (o script confere que nenhum saldo fica negativo).
saldo_final = {
    "PA-001": 0, "PA-002": 0, "SA-010": 10, "SA-020": 40,
    "MP-100": 60, "MP-101": 8, "MP-200": 30, "MP-201": 300,
    "MP-202": 18, "MP-300": 15, "MP-301": 8, "MP-302": 20, "MP-303": 6,
}

# (data, codigo, tipo, variacao com sinal, documento)
historico = [
    ("2026-10-01", "MP-202", "ENTRADA", 60, "NF 4521 - Pneus Minas"),
    ("2026-10-05", "MP-200", "SAIDA", -40, "OP-0003 (SA-020)"),
    ("2026-10-05", "MP-201", "SAIDA", -1440, "OP-0003 (SA-020)"),
    ("2026-10-05", "MP-202", "SAIDA", -40, "OP-0003 (SA-020)"),
    ("2026-10-05", "SA-020", "ENTRADA", 40, "OP-0003 (apontamento)"),
    ("2026-10-07", "MP-202", "AJUSTE", -2, "Inventario mensal"),
    ("2026-10-12", "MP-100", "ENTRADA", 100, "NF 4602 - Aco Minas"),
    ("2026-10-15", "MP-100", "SAIDA", -60, "OP-0002 (SA-010)"),
    ("2026-10-15", "MP-101", "SAIDA", -10, "OP-0002 (SA-010)"),
    ("2026-10-15", "SA-010", "ENTRADA", 20, "OP-0002 (apontamento)"),
    ("2026-10-20", "SA-010", "SAIDA", -10, "OP-0001 (PA-001)"),
    ("2026-10-20", "SA-020", "SAIDA", -20, "OP-0001 (PA-001)"),
    ("2026-10-20", "MP-300", "SAIDA", -10, "OP-0001 (PA-001)"),
    ("2026-10-20", "MP-301", "SAIDA", -10, "OP-0001 (PA-001)"),
    ("2026-10-20", "PA-001", "ENTRADA", 10, "OP-0001 (apontamento)"),
    ("2026-10-22", "PA-001", "SAIDA", -10, "Expedicao NF 9001"),
    ("2026-10-25", "MP-301", "AJUSTE", -2, "Inventario mensal"),
    ("2026-11-03", "MP-200", "ENTRADA", 30, "NF 4710 - Aros Brasil"),
]

# Saldo inicial = saldo final - soma das variacoes do historico
variacao_total = {}
for _, codigo, _, variacao, _ in historico:
    variacao_total[codigo] = variacao_total.get(codigo, 0) + variacao

movimentos_brutos = []
for codigo, final in saldo_final.items():
    inicial = final - variacao_total.get(codigo, 0)
    if inicial > 0:
        movimentos_brutos.append(
            ("2026-09-30", codigo, "ENTRADA", inicial, "Saldo inicial"))
movimentos_brutos += historico
movimentos_brutos.sort(key=lambda m: m[0])  # estavel: mantem a ordem

estoque = {}
movimentos = []
for data, codigo, tipo, variacao, documento in movimentos_brutos:
    saldo = round(estoque.get(codigo, 0) + variacao, 4)
    assert saldo >= 0, f"saldo negativo em {codigo} ({documento})"
    estoque[codigo] = saldo
    movimentos.append({"data": data, "codigo": codigo, "tipo": tipo,
                       "quantidade": variacao, "saldo": saldo,
                       "documento": documento})

for codigo, final in saldo_final.items():
    assert estoque.get(codigo, 0) == final, codigo
estoque = {c: s for c, s in estoque.items() if s > 0}

# --- Ordens ja existentes ---------------------------------------------
# Encerradas (historico do kardex), uma FIRME e tres LIBERADAS. O MRP
# vai gerar as demais (PLANEJADAS e ATRASADAS) em cima destas.


def ordem(numero, tipo, codigo, qtd, lib, ent, status):
    return {"numero": numero, "tipo": tipo, "item": codigo,
            "quantidade": qtd, "sem_liberacao": lib, "sem_entrega": ent,
            "status": status}


ordens = [
    ordem("OP-0001", "OP", "PA-001", 10, -4, -3, "ENCERRADA"),
    ordem("OP-0002", "OP", "SA-010", 20, -3, -2, "ENCERRADA"),
    ordem("OP-0003", "OP", "SA-020", 40, -2, -1, "ENCERRADA"),
    # FIRME: o MRP conta como recebimento programado (RN08)
    ordem("OP-0004", "OP", "SA-010", 20, 1, 2, "FIRME"),
    # LIBERADA sem componentes suficientes: o apontamento e rejeitado
    ordem("OP-0005", "OP", "SA-020", 80, 1, 2, "LIBERADA"),
    # LIBERADA com componentes: o apontamento funciona
    ordem("OP-0006", "OP", "SA-010", 10, 1, 2, "LIBERADA"),
    # OC liberada: pode ser recebida pelo menu de ordens
    ordem("OC-0001", "OC", "MP-100", 100, 1, 3, "LIBERADA"),
]

mps = {
    "PA-001": [0, 10, 30, 0, 20, 0, 0, 0],
    "PA-002": [0, 0, 15, 0, 0, 10, 0, 20],
}

salvar_tudo(itens, estrutura, estoque, mps, ordens, movimentos,
            centros, roteiros)
print("Base de demonstracao gravada em data/.")