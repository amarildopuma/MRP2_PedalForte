# Sistema MRP II — Pedal Forte Bicicletas

Projeto individual da disciplina de Programação em Python (CEFET-MG,
Campus Divinópolis, prof. Guido Pantuza). Sistema em modo texto que planeja
produção e compras de uma fábrica fictícia de bicicletas com MRP II: MPS,
estrutura de produto (BOM), estoques, MRP, ordens, carga x capacidade (CRP),
custo padrão, relatórios CSV e gráficos.

Autor: Amarildo

## Vídeos

- Demonstração do sistema em funcionamento: <[Assistir no YouTube](https://youtu.be/jZNEMW9X0CU)>
- Demonstração do código (arquitetura, estruturas de dados e decisões de
  projeto): <[Assistir no YouTube](https://youtu.be/RCgknTBK0uU)>

## Como executar

Requisitos: Python 3.10 ou superior (testado em Linux) e a biblioteca
`matplotlib` (só para os gráficos; o resto do sistema roda sem ela).

```bash
git clone <https://github.com/amarildopuma/MRP2_PedalForte>
cd MRP2_PedalForte
pip install -r requirements.txt
python3 carregar_demo.py     # carrega a base de demonstracao em data/
python3 main.py
```

`carregar_demo.py` é opcional: ele **sobrescreve** `data/` com a base de
demonstração (2 PA, 2 SA, 9 MP e 3 centros de trabalho). Sem ele o sistema
começa vazio. Os dados são carregados ao iniciar e salvos a cada alteração.

## Roteiro de uso (ciclo completo)

1. **MPS (3):** conferir ou cadastrar a demanda semanal dos PA.
2. **Executar MRP (4):** calcula e gera as ordens planejadas; "Ver registro"
   mostra as 6 linhas do MRP de um item.
3. **Ordens (5):** listar, **firmar** e **liberar** as ordens.
4. **Estoque (2):** dar entrada nas matérias-primas que faltam.
5. **Ordens (5) → Apontar produção:** baixa os componentes, dá entrada no
   item produzido e encerra a OP. Se faltar componente, rejeita.
   **Receber compra** faz o mesmo para uma OC (entrada da MP).
6. **CRP (6), Custo padrão (7), Relatórios (8), Gráficos (9).**

## Estrutura do projeto

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada |
| `menu.py` | Menu principal e submenus; mantém os dados em memória |
| `utils.py` | Leitura validada de entradas, formatação de datas e moeda |
| `itens.py` | Cadastro de itens (PA, SA, MP) |
| `estrutura.py` | BOM e explosão recursiva indentada |
| `estoque.py` | Movimentações, saldo e kardex |
| `mps.py` | Plano mestre de produção (8 semanas) |
| `mrp.py` | Cálculo das necessidades (MRP) |
| `ordens.py` | OPs, OCs, status e apontamento |
| `capacidade.py` | Centros de trabalho, roteiros e CRP |
| `custos.py` | Custo padrão (recursivo) |
| `relatorios.py` | Exportação em CSV |
| `graficos.py` | Gráficos de gestão (matplotlib) |
| `persistencia.py` | Leitura e gravação em JSON e CSV |
| `carregar_demo.py` | Carrega a base de demonstração |

## Estruturas de dados

- `itens = {codigo: {descricao, tipo, unidade, custo, lead_time,
  estoque_seguranca, lote_minimo}}`
- `estrutura = {pai: {filho: quantidade}}`
- `estoque = {codigo: saldo}`
- `movimentos = [{data, codigo, tipo, quantidade, saldo, documento}]`
- `mps = {codigo_pa: [demanda das 8 semanas]}`
- `ordens = [{numero, tipo, item, quantidade, sem_liberacao, sem_entrega,
  status}]`
- `centros = {codigo: {descricao, capacidade, custo_hora}}`
- `roteiros = {item: {centro, tempo}}` (tempo em horas por unidade)

Arquivos em `data/`: `itens.json`, `estrutura.json`, `estoque.json`,
`movimentos.csv`, `centros.json`, `roteiros.json`, `mps.json`,
`ordens.json`.

## Decisões de projeto

- **Programação estruturada, sem POO.** Dados em dicionários e listas,
  passados como parâmetro às funções.
- **BOM como dicionário de dicionários**, com explosão recursiva
  (`explodir_bom`) e custo recursivo (`calcular_custo_padrao`).
- **Kardex só cresce.** Correções são feitas com movimentos AJUSTE (RN10).
  O saldo nunca fica negativo (RN02): a checagem é feita antes de gravar.
- **Apontamento atômico.** Antes de mexer no estoque, o sistema verifica
  todos os componentes; se algum faltar, nada é alterado (RF11).
- **Ordens atrasadas.** Uma ordem com liberação antes da semana 1 é marcada
  ATRASADA e gera mensagem de exceção (RN07). Mesmo atrasada, ela continua
  gerando necessidade para os componentes, na semana 1.
- **Carga do CRP (RN09).** Soma, por semana de liberação, quantidade ×
  tempo unitário das OPs ainda não encerradas. OP atrasada conta na
  semana 1. Há sobrecarga quando a carga supera a capacidade.
- **Custo padrão (RF13).** MP usa o custo cadastrado. PA e SA = soma
  (quantidade × custo padrão do componente) + mão de obra (tempo do
  roteiro × custo-hora do centro). Para PA e SA, o custo digitado no
  cadastro não entra na conta.
- **Persistência.** JSON para o cadastro e CSV para o kardex.
- **Gráficos.** Salvos em `graficos/` (PNG) e exibidos na tela. Se o
  matplotlib não estiver instalado, só os gráficos ficam indisponíveis.
- **Relatórios.** CSVs gravados em `exportacoes/`.

## Como o MRP é calculado

1. Itens processados em ordem: PA, depois SA, depois MP (RN04).
2. Necessidade bruta: do PA vem do MPS; do SA e da MP vem das liberações
   planejadas dos pais × quantidade na BOM.
3. Para cada semana:
   - NL = max(0, NB + estoque de segurança − (EP anterior + RP)) (RN05);
   - recebimento planejado = max(NL, lote mínimo) (RN06);
   - liberação planejada = semana do recebimento − lead time (RN07).
4. Só ordens FIRME e LIBERADA contam como recebimento programado; as
   PLANEJADAS e ATRASADAS são apagadas e recalculadas a cada execução
   (RN08).

Status das ordens: PLANEJADA → FIRME → LIBERADA → ENCERRADA.

## Requisitos funcionais

| RF | Onde |
|---|---|
| RF01 menu | `menu.py` |
| RF02 itens | `itens.py` |
| RF03 BOM indentada | `estrutura.py` |
| RF04 movimentações | `estoque.registrar_movimentacao` |
| RF05 saldo, kardex, alerta | `estoque.exibir_kardex` |
| RF06 centros e roteiros | `capacidade.py` |
| RF07 MPS | `mps.py` |
| RF08 registro MRP | `mrp.executar_mrp`, `mrp.exibir_registro_mrp` |
| RF09 ordens planejadas | `mrp.gerar_ordens_do_registro` |
| RF10 firmar, liberar, encerrar | `ordens.py` |
| RF11 apontar produção | `ordens.apontar_producao` |
| RF12 CRP | `capacidade.exibir_crp` |
| RF13 custo padrão | `custos.py` |
| RF14 CSV | `relatorios.py` |
| RF15 persistência | `persistencia.py` |
| RF16 gráficos | `graficos.py` |

## Regras de negócio

| Regra | Onde |
|---|---|
| RN01 código único Tipo-Número | `itens.cadastrar_item`, `utils.validar_codigo` |
| RN02 saldo nunca negativo | `estoque.registrar_movimentacao` |
| RN03 BOM em até 3 níveis | `estrutura.validar_componente` |
| RN04 PA → SA → MP | `mrp.ordenar_itens_por_tipo` |
| RN05 a RN07 | `mrp.calcular_registro_item` |
| RN08 recebimentos programados | `mrp.obter_recebimentos_programados`, `ordens.apagar_ordens_planejadas` |
| RN09 carga do centro | `capacidade.calcular_carga` |
| RN10 kardex imutável | `estoque.py` (só existe `append`) |

## Uso de inteligência artificial

- Este Readme foi gerado por IA(Claude)
- Além disso, a base de carregamento também foi feito por ele e 
- Testes para ver se o código quebraria 


## Limitações conhecidas

- Os registros do MRP ficam só em memória: depois de reabrir o sistema é
  preciso executar o MRP de novo para vê-los (as ordens ficam salvas).
- Os números das ordens PLANEJADAS e ATRASADAS mudam a cada execução do MRP,
  porque elas são apagadas e recriadas (RN08).