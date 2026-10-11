import os
import sys
import unittest


class TeeStream:
    """Duplica a saída para enviar simultaneamente ao console e ao arquivo de log."""
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
            s.flush()

    def flush(self):
        for s in self.streams:
            s.flush()


def run_suite():
    # 1. Garante que os caminhos sejam relativos à pasta onde este script está salvo
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # 2. Solicita identificação da fase para o nome do log
    try:
        fase_atual = input("Insira a fase atual para personalizar o log (ou ENTER para 'geral'): ").strip()
    except (EOFError, KeyboardInterrupt):
        fase_atual = "geral"

    if not fase_atual:
        fase_atual = "geral"

    # Sanitiza o nome do arquivo
    safe_fase = "".join(c for c in fase_atual if c.isalnum() or c in ("_", "-")).strip() or "geral"

    # 3. Garante a criação absoluta da pasta logs
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, f"log_{safe_fase}.txt")

    # 4. Carrega a suíte de testes com caminho absoluto
    loader = unittest.TestLoader()
    try:
        # Carrega diretamente o módulo test_combat para evitar falhas de discovery
        suite = loader.loadTestsFromName("test_combat")
    except Exception:
        # Fallback para discovery absoluto
        suite = loader.discover(start_dir=project_root, pattern="test_*.py")

    print(f"\nIniciando execução da suíte de testes...")
    print(f"Diretório base: {project_root}")
    print(f"Arquivo de log: {log_path}\n" + "-" * 50)

    # 5. Executa os testes gravando no arquivo e transmitindo ao terminal
    with open(log_path, "w", encoding="utf-8") as log_file:
        tee = TeeStream(sys.stdout, log_file)
        
        # Redireciona stdout e stderr durante os testes para capturar prints e relatórios
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = tee
        sys.stderr = tee

        try:
            runner = unittest.TextTestRunner(stream=tee, verbosity=2)
            result = runner.run(suite)
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    print("-" * 50)
    print(f"Execução concluída!")
    print(f"Logs salvos com sucesso em: {log_path}")
    print(f"Total executados: {result.testsRun} | Falhas: {len(result.failures)} | Erros: {len(result.errors)}")

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    run_suite()
