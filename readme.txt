# 📊 Dashboard Interativo para Planilhas Excel – SERIN

Este projeto consiste em um **dashboard interativo desenvolvido em Python** para análise de dados provenientes de planilhas Excel.
A aplicação permite que o usuário envie múltiplas planilhas e navegue por diferentes páginas de análise como **Visão Geral, Órgãos, Municípios, Tempo e Dados brutos**.

O sistema foi desenvolvido utilizando **Streamlit**, permitindo criar uma interface web interativa de forma rápida e simples.

---

# 🎯 Objetivo do Projeto

O objetivo do projeto é facilitar a **visualização e exploração de dados de planilhas Excel**, permitindo:

* Upload de uma ou mais planilhas
* Leitura automática das abas relevantes
* Aplicação de filtros globais
* Visualização de indicadores (KPIs)
* Navegação entre diferentes perspectivas dos dados
* Exploração detalhada dos registros

Isso possibilita transformar dados de planilhas em **informação visual e navegável**.

---

# 🛠 Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

### Linguagem

* **Python 3**

### Framework Web

* **Streamlit**
  Utilizado para construir a interface web interativa do dashboard.

### Manipulação de Dados

* **Pandas**
  Responsável pelo carregamento, tratamento e filtragem dos dados.

### Leitura de Planilhas

* **OpenPyXL / Excel Engine**
  Utilizado pelo pandas para leitura de arquivos `.xlsx`.

---

# 📂 Estrutura do Projeto

```
dashboard_excel/
│
├── app.py
├── requirements.txt
│
├── .streamlit/
│   └── config.toml
│
├── pages/
│   ├── 1_Visao_Geral.py
│   ├── 2_Orgaos.py
│   ├── 3_Municipios.py
│   ├── 4_Tempo.py
│   └── 5_Dados.py
│
└── src/
    ├── charts.py
    ├── data_io.py
    ├── processing.py
    └── ui.py
```

### Descrição dos principais arquivos

#### `app.py`

Arquivo principal da aplicação.
Responsável por:

* configurar a página
* carregar os dados
* exibir KPIs iniciais
* controlar o fluxo do dashboard.

---

#### `pages/`

Contém as páginas adicionais do Streamlit.

Cada arquivo representa uma aba do dashboard:

| Página      | Função                        |
| ----------- | ----------------------------- |
| Visão Geral | Panorama geral dos dados      |
| Órgãos      | Análise por órgão             |
| Municípios  | Análise por município         |
| Tempo       | Análise temporal              |
| Dados       | Visualização da base completa |

---

#### `src/ui.py`

Contém componentes de interface como:

* Sidebar para upload de planilhas
* Filtros globais
* Exibição de KPIs

---

#### `src/data_io.py`

Responsável por:

* leitura das planilhas
* detecção automática das abas válidas
* consolidação das bases de dados

---

#### `src/processing.py`

Realiza o **tratamento e preparação dos dados**, incluindo:

* limpeza de colunas
* padronização
* aplicação de filtros globais

---

#### `src/charts.py`

Contém funções responsáveis pela geração dos **gráficos e visualizações do dashboard**.

---

# ⚙️ Como Executar o Projeto

## 1️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 2️⃣ Executar o dashboard

```bash
streamlit run app.py
```

ou

```bash
python3 -m streamlit run app.py
```

---

## 3️⃣ Abrir no navegador

Após iniciar o servidor, o Streamlit exibirá algo como:

```
Local URL: http://localhost:8501
```

Abra esse endereço no navegador para acessar o dashboard.

---

# 📥 Como Utilizar o Dashboard

1. Abra o sistema no navegador
2. Faça upload de uma ou mais planilhas Excel na **barra lateral**
3. O sistema detectará automaticamente as abas com o formato esperado
4. Utilize os filtros globais disponíveis
5. Navegue entre as páginas para explorar os dados

---

# 📊 Funcionalidades do Dashboard

✔ Upload de múltiplas planilhas
✔ Consolidação automática dos dados
✔ Filtros globais aplicados em todas as páginas
✔ KPIs rápidos na página inicial
✔ Navegação por múltiplas visões dos dados
✔ Visualização de dados brutos

---

# 🚀 Possíveis Melhorias Futuras

* Integração com banco de dados
* Exportação de relatórios em PDF
* Novos gráficos interativos
* Sistema de autenticação de usuários
* Deploy em servidor ou nuvem

---

# 👨‍💻 Autor

Projeto desenvolvido por **Cleriston Pereira da Silva Junior**.
