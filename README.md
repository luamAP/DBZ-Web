# 🐉 Dragon Ball Z Text Battle (Python CLI)

Um simulador de combate por turnos no universo de Dragon Ball Z, concebido sob os princípios de **Clean Code**, **SOLID** e arquitetura estritamente **Orientada a Dados (Data-Driven)**.

---

## 🏗️ Arquitetura do Projeto

O ecossistema é projetado sob os princípios de **Clean Code**, **SOLID** e uma arquitetura estritamente **Orientada a Dados (Data-Driven)**, desacoplando regras matemáticas e catálogo de entidades do código de execução da aplicação.

Para a documentação completa dos componentes, contratos de dados, fluxo de dependências e responsabilidades de cada módulo:
👉 **[Documentação Arquitetural Completa (`arquitetura.md`)](arquitetura.md)**

---

## 🛠️ Extensão de Personagens

O ecossistema é totalmente orientado a dados, permitindo a inclusão de lutadores sem alteração no código Python.

Para consultar a especificação completa dos campos, regras de balanceamento de técnicas e copiar o template YAML pronto para uso, consulte:
👉 **[Guia de Criação de Personagens (`character_template.md`)](docs/character_template.md)**

---

## 🧪 Execução e Testes Automatizados

### Executar o Jogo

```bash
python main.py
```

### Executar a Suíte de Testes com `run_tests.py`

Para rodar os testes e gerar os logs de forma automática:

Exemplo de execução:

```bash
python run_tests.py fase4
```

* O script garante a existência da pasta `logs/` e salva o relatório detalhado em `logs/log_<fase>.txt`.

### Executar via Terminal Manualmente

```bash
python -m unittest discover tests
```

Para redirecionar manualmente para o arquivo de log:

* **Linux / macOS / Git Bash:**

  ```bash
  mkdir -p logs
  python -m unittest discover tests > logs/log.txt 2>&1
  ```

* **Windows (PowerShell):**

  ```powershell
  if (!(Test-Path "logs")) { New-Item -ItemType Directory -Name "logs" }
  python -m unittest discover tests *>&1 | Out-File -FilePath logs/log.txt
  ```

### Executar via Interface Gráfica da IDE

1. **VS Code:** Abra o painel de **Testing** (ícone de tubo de ensaio), configure para `unittest` na pasta de testes e execute pelo painel.
2. **PyCharm:** Clique com o botão direito sobre o diretório de testes ou `run_tests.py` e escolha **Run**.
