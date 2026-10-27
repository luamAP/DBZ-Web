import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

MAX_TRACE_LINES = 12  # linhas finais de cada traceback exibidas no console


def _resolve_phase(args):
    """Lê a fase via argumento (posicional ou -f/--fase) ou pergunta, se interativo."""
    phase = "geral"
    if args and not args[0].startswith("-"):
        phase = args[0]
    elif len(args) > 1 and args[0] in ("-f", "--fase", "--phase"):
        phase = args[1]
    elif sys.stdin.isatty():
        try:
            phase = input("Fase para o nome do log (ENTER = 'geral'): ").strip() or "geral"
        except (EOFError, KeyboardInterrupt):
            pass
    return "".join(c for c in phase if c.isalnum() or c in "_-") or "geral"


def _tail(text, limit=MAX_TRACE_LINES):
    lines = text.strip().splitlines()
    if len(lines) <= limit:
        return "\n".join(lines)
    return "  ...\n" + "\n".join(lines[-limit:])


def run_suite():
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    phase = _resolve_phase(sys.argv[1:])
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, f"log_{phase}.txt")

    suite = unittest.TestLoader().discover(
        start_dir=os.path.join(project_root, "tests"),
        pattern="test_*.py",
        top_level_dir=project_root,
    )

    # Relatório detalhado e prints do código testado vão SOMENTE para o arquivo.
    with open(log_path, "w", encoding="utf-8") as log_file, \
            redirect_stdout(log_file), redirect_stderr(log_file):
        result = unittest.TextTestRunner(stream=log_file, verbosity=2).run(suite)

    problems = [("FAIL", t, tb) for t, tb in result.failures]
    problems += [("ERROR", t, tb) for t, tb in result.errors]

    status = "OK" if result.wasSuccessful() else "FALHOU"
    print(f"{status}: {result.testsRun} testes | {len(result.failures)} falhas | "
          f"{len(result.errors)} erros | {len(result.skipped)} ignorados")
    for kind, test, trace in problems:
        print(f"\n[{kind}] {test.id()}\n{_tail(trace)}")
    print(f"\nLog completo: {log_path}")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_suite())
